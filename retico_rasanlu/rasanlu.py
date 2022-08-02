"""A module for Natural Language Understanding provided by rasa_nlu"""

# retico
from retico_core import abstract
from retico_core.text import SpeechRecognitionIU
from retico_core.dialogue import DialogueActIU

# rasa
import sys
import os
import asyncio
from functools import wraps, partial
# sys.path.append(os.environ['RASA'])
# from rasa.nlu.model import IncrementalInterpreter as Interpreter
from rasa.core.agent import Agent, load_agent

class RasaNLUModule(abstract.AbstractModule):
    """A standard rasa NLU module.

    Attributes:
        model_dir (str): The path to the directory of the NLU model generated by
            rasa_nlu.train.
        config_file (str): The path to the json file containing the rasa nlu
            configuration.
    """

    @staticmethod
    def name():
        return "Rasa NLU Module"

    @staticmethod
    def description():
        return "A Module providing Natural Language Understanding by rasa_nlu"

    @staticmethod
    def input_ius():
        return [SpeechRecognitionIU]

    @staticmethod
    def output_iu():
        return DialogueActIU

    def __init__(self, model_dir, incremental=True, **kwargs):
        """Initializes the RasaNLUModule.

        Args:
            model_dir (str): The path to the directory of the NLU model
                generated by rasa_nlu.train.
        """
        super().__init__(**kwargs)
        self.model_dir = model_dir
        self.interpreter = None
        self.incremental = incremental
        self.lb_hypotheses = []
        self.cache = None
        self.started_prediction = False
        self.prefix = []
        self.load_latest_model()

    def load_latest_model(self):
        files = os.listdir(self.model_dir) 
        paths = [os.path.join(self.model_dir, basename) for basename in files] 
        latest_file = max(paths, key=os.path.getctime) 
        print("NLU loading latest file", latest_file)
        self.interpreter =  Agent.load(model_path=latest_file)   
    
    def new_utterance(self):
        if self.incremental:
            self.interpreter.new_utterance()
        self.prefix = []
        super().new_utterance()

    def process_result(self, result, input_iu):
        #print("RESULT: {}".format(result))
        payload = {}
        for entity in result.get("entities"):
            payload[entity["entity"]] = entity["value"]
            # concepts['{}_confidence'.format(entity["entity"])] = entity['confidence']
        act = result["intent"]["name"]
        # confidence = result["intent"]["confidence"]
        # print('nlu', act, concepts, confidence)
        output_iu = self.create_iu(input_iu)
        output_iu.payload = payload
        piu = output_iu.previous_iu
        if input_iu.committed:
            output_iu.committed = True
            self.started_prediction = False
        else:
            self.started_prediction = True
        update_iu = abstract.UpdateMessage()
        update_iu = abstract.UpdateMessage.from_iu(output_iu, abstract.UpdateType.ADD)            
        return update_iu

    def process_update(self, update_message):
        print("NLU getting update")
        result = ""
        for iu,um in update_message:
            if um == abstract.UpdateType.ADD:
                self.process_iu(iu)
            elif um == abstract.UpdateType.REVOKE:
                self.process_revoke(iu)


    def process_iu(self, input_iu):
        if self.incremental:
            result = None
            for word in input_iu.get_text().split():
                text_iu = (word, "add") # only handling add for now
                result = self.interpreter.parse_incremental(text_iu)
        else:
            self.prefix.append(input_iu.get_text())
            text = ' '.join(self.prefix)
            # we need to do some shananigans to make the async RASA interpreter work in a synchronous function
            async def async_interpret(text):
                result = await self.interpreter.parse_message(message_data=text)
                if result is not None:
                    p_result = self.process_result(result, input_iu)
                    self.append(p_result)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            coroutine = async_interpret(text)
            loop.run_until_complete(coroutine)
        

    def process_revoke(self, revoked_iu):
        
        result =  None
        if self.incremental:
            for word in reversed(revoked_iu.get_text().split()):
                text_iu = (word, "revoke") 
                # print('nlu revoke({})'.format(word))
                result = self.interpreter.parse_incremental(text_iu)
            if result is not None:
                result = self.process_result(result, revoked_iu)
        else:
            if len(self.prefix) > 0:
                self.prefix.pop()
            
        if len(self._iu_stack) > 0:
            last_output_iu = self._iu_stack.pop()
            self.revoke(last_output_iu)
        
        return result

    def setup(self):
        pass


