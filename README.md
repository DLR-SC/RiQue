# Island-Voiz

## Dependencies 

* raumel.yaml (pip3 install ruamel.yaml)
* py2neo (conda install -c conda-forge py2neo)
* pip3 install python_cypher
* pip3 install rasa_nlu
* pip3 install rasa_nlu[spacy]
* python -m spacy download en_core_web_md
* python -m spacy link en_core_web_md en
* pip3 install rasa_nlu[tensorflow]
* [Install neo4j ubuntu 16.04](https://datawookie.netlify.com/blog/2016/09/installing-neo4j-on-ubuntu-16.04/)
* * Start neo4j server using ```sudo service neo4j start```
* * Stop neo4j server using ```sudo service neo4j stop```
* * To restart neo4j server ```sudo service neo4j restart```

## Steps

* First convert json to neo4j by executing ```neo4j/JsonToNeo4j.ipynb``` (Remember to start the neo4j server and configure it)
* In one terminal: Run ``` python  train_rasa_module.py 'train-all' ``` to train and save the rasa nlu and core models
   **If models are already saved, then you this step is optional**
* In second terminal: Run action server using ``` python  train_rasa_module.py 'train-all' ```
* In third terminal: Pass user messages and end points to rasa core using:
    ``` python -m rasa_core.run -d models/dialogue -u projects/default/default/Neo4jNlu --endpoints endpoints.yml ```
* Now you can pass the messages to the bot and wait for the responses 

## Files Details

* ```nlu.json``` contains the training data for rasa nlu part
* ```nlu.config``` contains the configuration files of rasa nlu
* ```domain.yml``` defines the templates, intents, actions for the bot. These are used by rasa core
* ```stories.md``` tells the bot what actions to take during the dialogue. In other words, it is a training data for the dialogue system 
* ```actions.py``` has information about custom actions
* ```endpoints.yml``` defines the action end point using url 
* ```restaurants.txt``` has list of restaurants, that are fetched by actions
* ```queryGeneration.py``` helps bot to generate query based on predicted intents and entities
* ```train_nlu.py``` trains the nlu and stores the model in directory: ```projects/default/default/Neo4jNlu```
* ```train_rasa_module.py``` trains rasa core and nlu with command line input ```python  train_rasa_module.py 'train-all' ```
     and saves the trained model. Rasa core model is saved in ```models/dialogue```

## General Conversation Examples

### Conversation 1
  
```
* User: Hi
* Response by bot: Hey, How can I help you? 
* Possible question by User:  I am looking for restaurants in bonn 
* Response by bot: List of resturants are: pizza hut, kfc, mcdonalds 
* User :  Give me details of pizza hut 
* Response by bot:  It is located near HBF 
* User: Bye
* Bot response: Bye
```

### Conversation 2 (Generate queries related to RCE project)

```
* User: show me information of rce input provider component gui bundles
* Reponse by bot: Outputs result of query 

```

* **Note:** Till now queries are only implemented related to bundles
.
