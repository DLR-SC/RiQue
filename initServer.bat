@echo off
start /wait python -m rasa_core.train -d domain.yml -s stories.md -o models/dialogue
start /wait python -m rasa_nlu.train -c nlu_config.yml --data nlu.md -o models --fixed_model_name nlu --project current --verbose
start python -m rasa_core.run -d models/dialogue --enable_api -u models/current/nlu --credentials credentials.yml --endpoints endpoints.yml -o out.log