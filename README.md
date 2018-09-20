1. Write nlu.md
2. write domain.yml
3. writer stories.md
4. write nlu_config.yml

(in Anaconda prompt)

5. if not already done: pip install rasa_core
6. 'pip install rasa_nlu[spacy]
python -m spacy download en_core_web_md
python -m spacy link en_core_web_md en'
7. Train Dialogue:
python -m rasa_core.train -d domain.yml -s stories.md -o models/dialogue

8. Train NLU:
python -m rasa_nlu.train -c nlu_config.yml --data nlu.md -o models --fixed_model_name nlu --project current --verbose

9. run nlu server:
python -m rasa_core.run -d models/dialogue --enable_api -u models/current/nlu --credentials credentials.yml --endpoints endpoints.yml -o out

10. run action server:
python -m rasa_core_sdk.endpoint --actions actions

11. query your webservice:
curl -XPOST -H "Content-Type: application/json" http://localhost:5005/webhooks/rest/webhook -d "{\"sender\":\"default\",\"message\":\"hello\"}"
Troubleshoot:
- pip install service_identity