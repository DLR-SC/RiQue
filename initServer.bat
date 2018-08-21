@echo off
start /wait python -m rasa_core.train -d domain.yml -s stories.md -o models/dialogue
start /wait python -m rasa_nlu.train -c nlu_config.yml --data nlu.md -o models --fixed_model_name nlu --project current --verbose
start /wait python -m rasa_core.server -d models/dialogue -u models/current/nlu -o out.log