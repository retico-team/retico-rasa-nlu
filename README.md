# retico-rasa-nlu
ReTiCo Module for RASA NLU

### Dependencies

`pip install rasa==3.0.0`

### Code Example

```
from retico_rasanlu import RasaNLUModule
from retico_googleasr.googleasr import GoogleASR

asr = GoogleASR()
model_dir = 'models/nlu_20220519-154621'
nlu = RasaNLUModule(model_dir=model_dir, incremental=False)

asr.subscribe(nlu)
nlu.subscribe(...)

asr.run()
nlu.run()
```
