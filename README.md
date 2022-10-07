# retico-rasa-nlu
ReTiCo Module for RASA NLU

### Dependencies

`rasa==3.0.0`

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

Citation
```

@ARTICLE{Bocklisch2017-ez,
  title    = "Rasa: Open Source Language Understanding and Dialogue Management",
  author   = "Bocklisch, Tom and Faulkner, Joey and Pawlowski, Nick and Nichol,
              Alan",
  abstract = "We introduce a pair of tools, Rasa NLU and Rasa Core, which are
              open source python libraries for building conversational
              software. Their purpose is to make machine-learning based
              dialogue management and language understanding accessible to
              non-specialist software developers. In terms of design
              philosophy, we aim for ease of use, and bootstrapping from
              minimal (or no) initial training data. Both packages are
              extensively documented and ship with a comprehensive suite of
              tests. The code is available at https://github.com/RasaHQ/",
  journal  = "Proceedings of the 31st Conference on Neural Information
              Processing Systems",
  year     =  2017,
  address  = "Long Beach, CA"
}
```
