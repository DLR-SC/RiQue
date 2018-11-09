# Island-Voiz

## Dependencies 

* raumel.yaml (pip3 install ruamel.yaml)
* py2neo (conda install -c conda-forge py2neo)
* pip3 install python_cypher
* pip3 install rasa_nlu
* pip3 install rasa_nlu[spacy]
* pip3 install rasa_core
* python -m spacy download en_core_web_md
* python -m spacy link en_core_web_md en
* pip3 install rasa_nlu[tensorflow]
* [Install neo4j ubuntu 16.04](https://datawookie.netlify.com/blog/2016/09/installing-neo4j-on-ubuntu-16.04/)
* * Start neo4j server using ```sudo service neo4j start```
* * Stop neo4j server using ```sudo service neo4j stop```
* * To restart neo4j server ```sudo service neo4j restart```

## Installation

For easier installation, clone this repository, create new python 3 environment and execute: ```pip install -r requirements.txt```

To install neo4j follow: [Installation neo4j guidelines](https://datawookie.netlify.com/blog/2016/09/installing-neo4j-on-ubuntu-16.04/)
## Steps

* First convert json to neo4j by executing ```neo4j/JsonToNeo4j.ipynb``` (Remember to start the neo4j server and configure it)
* In one terminal: Run ``` python  train_rasa_module.py 'train-all' ``` to train and save the rasa nlu and core models
   **If models are already saved, then this step is optional**
* In second terminal: Run action server using ``` python -m rasa_core_sdk.endpoint --actions actions ```
* In third terminal: Pass user messages and end points to rasa core using:
    ``` python -m rasa_core.run -d models/dialogue -u projects/default/default/Neo4jNlu --endpoints endpoints.yml ```
* Now you can pass the messages to the bot and wait for the responses 

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

## General Conversation Examples


### Conversation 1 (search information of node with name)

```
* User: show me details of remote component environment node
* Reponse by bot: Outputs result of query 

* User: give me info of database node
* Reponse by bot: Outputs result of query 

```

### Conversation 2 (search information of node based on string matching (user don't have to include complete name) )

```
* User: show me details of remote component node
* Reponse by bot: Outputs information of all nodes that starts with **remote component**


```

### Conversation 3 (Show all the nodes) 

```
* User: show all the bundles units
* Response by bot: Outputs all bundles in the project

* User: show all the packages units
* Response by bot: Outputs all packages in the project

* User: show all the compilation units
* Response by bot: Outputs all compilation units in the project

* User: show all the services
* Response by bot: Outputs all services in the project

```


### Conversation 4 (count all the nodes) 

```
* User: give me count of all the bundles units
* Response by bot: Outputs count of all bundles in the project

* User: find count of all the packages units
* Response by bot: Outputs count of all packages in the project

* User: find count of all compilation units
* Response by bot: Outputs count of compilation units in the project

* User: give me count of all the services units
* Response by bot: Outputs count of all services in the project

```

### Conversation 5 (Show information related to specific bundle) 

```
* User: find imports of rce cluster component gui bundle
* Response by bot: Outputs imports of rce cluster component gui  bundles in the project

* User: find packages of rce cluster component gui bundle
* Response by bot: Outputs packages of rce cluster component gui bundle

* User: find components of rce components doe execution bundle
* Response by bot: Outputs components of rce components doe execution bundle

* User: give compilation units of rce xml loader component gui
* Response by bot: Outputs compilation units of rce xml loader component gui

* User: show exports of rce components doe execution bundle
* Response by bot: Outputs exports of rce components doe execution bundle

```

### Conversation 6 (Show methods of specific bundle) 

```
* User: find methods of rce cluster component gui bundle
* Response by bot: Outputs methods name 

* User: show methods of rce xml loader component gui bundle
* Response by bot: Outputs methods name 

* User: give methods of rce components doe execution bundle
* Response by bot: Outputs methods name 

```

