# SentenceToQuery 

This component takes input in the form of text, uses [RASA](https://rasa.com/) library to predict the intents and entities, based on predicted intents, 
custom actions are executed and [pypher](https://github.com/emehrkay/Pypher) library is used to convert sentences in the form of neo4j Queries.

## Files Details

* ```nlu.json``` contains the training data for rasa nlu part
* ```nlu_config.yml``` contains the configuration files of rasa nlu
* ```domain.yml``` defines the templates, intents, actions for the bot. These are used by rasa core
* ```stories.md``` tells the bot what actions to take during the dialogue. In other words, it is a training data for the dialogue system 
* ```actions.py``` has information about custom actions
* ```endpoints.yml``` defines the action end point using url 
* ```queryGeneration.py``` helps bot to generate query based on predicted intents and entities
* ```train_nlu.py``` trains the nlu and stores the model in directory: ```projects/default/default/Neo4jNlu```
* ```train_rasa_module.py``` trains rasa core and nlu with command line input ```python  train_rasa_module.py 'train-all' ```
     and saves the trained model. Rasa core model is saved in ```models/dialogue```
* ```utils.py``` contains utility functions
