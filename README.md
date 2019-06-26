# RiQue (Request into Query)

This system take input as request/command and returns neo4j graph database query. This query is then sent to the Hololens which is connected with the neo4j graph database and as a response, result of a query is displayed on the hololens. However, this system can also be used independently. For that, user has to execute [Json File To Neo4j database](https://github.com/DLR-SC/RiQue/blob/master/neo4j/JsonToNeo4j.py) file which creates neo4j database in user's local system. After that database is queried based on output of RiQue and results are returned. Following diagram explains the input and output of the RiQue:

<p align="center">
  <img width="480" height="68" src="./images/RiQue_diagram.jpg">
</p>

## Installation

This project is developed and tested in Ubuntu 16.04

For easier installation, clone this repository, create new ```python 3.6``` environment and execute: ```pip install -r requirements.txt```

To install spacy language module: ```python -m spacy download en```

To install rasa: ```pip install rasa```

To install neo4j follow: [Installation neo4j guidelines in Ubuntu 16.04](https://datawookie.netlify.com/blog/2016/09/installing-neo4j-on-ubuntu-16.04/)

The chatbot models and files are maintained in ```SentenceToQuery```, whereas the property graphs are stored in ```neo4j``` folder

## Steps

* Start neo4j server ```service neo4j start```
* Convert json to neo4j by executing ```neo4j/JsonToNeo4j.py``` with python
* Navigate to SentenceToQuery directory and execute ```rasa train``` to train the chatbot model
* Now run action server using ```rasa run actions```
* Open another terminal and execute the chatbot ```rasa shell```

*The bot is ready to chat with you*

## Information about how sentences are converted to Neo4j query can be found here: ![SentenceToQuery](https://github.com/DLR-SC/RiQue/tree/master/SentenceToQuery)

## General Conversation Examples

### Conversation 1 (show information about current project) 

```
* User: Show the information of current project
* Response by bot: Outputs details about rce project

* User: Give info of current working project
* Response by bot: Outputs details about rce project

```
### Conversation 2 (search information of node with name)

```
* User: show me details of remote component environment node
* Reponse by bot: Outputs result of query 

* User: give info of database node
* Reponse by bot: Outputs result of query 

```

### Conversation 3 (search information of node based on string matching (user don't have to include complete name) )

```
* User: show me details of remote component node
* Reponse by bot: Outputs information of all nodes that starts with **remote component**


```

### Conversation 4 (Show all the nodes) 

```
* User: show all the bundles units
* Response by bot: Outputs all bundles in the project

* User: show me all island units
* Response by bot: Outputs all bundles in the project

* User: show all the packages units
* Response by bot: Outputs all packages in the project

* User: show all the regions
* Response by bot: Outputs all packages in the project


* User: show all the compilation units
* Response by bot: Outputs all compilation units in the project

* User: show all the building units
* Response by bot: Outputs all compilation units in the project

* User: show all the services
* Response by bot: Outputs all services in the project

```


### Conversation 5 (count all the nodes) 

```
* User: give me count of all the bundles units
* Response by bot: Outputs count of all bundles in the project

* User: find count of all the packages units
* Response by bot: Outputs count of all packages in the project

* User: find count of all the regions 
* Response by bot: Outputs count of all packages in the project

* User: find count of all compilation units
* Response by bot: Outputs count of compilation units in the project

* User: find count of all buildings
* Response by bot: Outputs count of compilation units in the project

* User: give me count of all the services units
* Response by bot: Outputs count of all services in the project

```

### Conversation 6 (Show information related to specific bundle) 

```
* User: find imports of rce cluster component gui bundle
* Response by bot: Outputs imports of rce cluster component gui  bundles in the project

* User: show imports of rce cluster component gui island
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

### Conversation 7 (Show methods of specific bundle) 

```
* User: find methods of rce cluster component gui bundle
* Response by bot: Outputs methods name 

* User: show methods of rce xml loader component gui bundle
* Response by bot: Outputs methods name 

* User: give methods of rce components doe execution bundle
* Response by bot: Outputs methods name 

```

### Conversation 8 (Show largest Compilation Unit  in bundle based on code lines) 

```
* User: find bundle with largest compilation unit
* Response by bot: Outputs bundle name with number of lines of code

* User: find largest compilation unit in rce xml loader component execution bundle 
* Response by bot: Outputs bundle largest compilation unit in this bundle


* User: show largest compilation unit
* Response by bot: Outputs bundle name with number of lines of code

* User: give compilation unit with highest lines of code
* Response by bot: Outputs methods name 
```

### Conversation 9 (Show Compilation Unit with highest number of methods) 

```
* User: find compilation unit with highest number of methods
* Response by bot: Outputs bundle name, compilation unit and total number of methods

* User: show compilation unit with most methods
* Response by bot: Outputs bundle name, compilation unit and total number of methods
```
