1. Write nlu.md
2. write domain.yml
3. writer stories.md
4. write nlu_config.yml

(in Anaconda prompt)
5. if not already done: pip install rasa_core
6. Train Dialogue:
python -m rasa_core.train -d domain.yml -s stories.md -o models/dialogue

7. Train NLU:
python -m rasa_nlu.train -c nlu_config.yml --data nlu.md -o models --fixed_model_name nlu --project current --verbose

8. run 
python -m rasa_core.server -d models/dialogue -u models/current/nlu -o out.log

9. talk to your webservice. Example:
curl -X POST localhost:5005/conversations/deafult/parse -d "{\"query\":\"hello\"}"