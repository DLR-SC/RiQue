import pypher

from pypher import Pypher, __
from pypher.builder import Param
from neo4j.v1 import GraphDatabase
from train_core_init import TrainBot
from rasa_core.interpreter import RasaNLUInterpreter

import json 

class GenerateQuery:
    
    def __init__(self, sentence):
        
        # self.interpret = Interpreter.load(train.model_directory)
        self.trainedBot = TrainBot()
        self.interpret = RasaNLUInterpreter(self.trainedBot.model_path_nlu)

        # self.interpret = interpreter
        self.extracted_intents = None
        self.extracted_entities = None
        self.extracted_values = None # entities values
        self.prediction = None
        self.pypherObject = Pypher()
        self.uri = "bolt://localhost:7687"
        self.driver = GraphDatabase.driver(self.uri, auth=("neo4j", "123456"))
        self.sentence = sentence
        
    def predictIntentionAndEntity(self):
        
        self.prediction = self.interpret.parse(self.sentence)
        
        if len(self.prediction.get("entities")) > 0:
            
            self.extracted_entities = self.prediction.get("entities")[0]['entity']
            self.extracted_values = self.prediction.get("entities")[0]['value']
            self.start_position = self.prediction.get("entities")[0]['start']
            self.end_position = self.prediction.get("entities")[0]['end']
            
#             print (self.extracted_values)

        self.extracted_intents = self.prediction.get("intent")['name']

        print ("Intent: ", self.extracted_intents)
        print ("entity type: ", self.extracted_entities)
        print ("entity value: ", self.extracted_values)
        print ("=======================================")
        print(json.dumps(self.prediction, indent=2))

        return self.prediction
    
    def convertTextToQuery(self, bundle_slot=None):


        query = None
        result = None
        query_result = None
        params = None

        if self.extracted_intents == 'showProjectInformation':
            
            
            # p.CREATE.node('user', 'User', Name='Jim')
            # p.Match.node('a', labels='bundles').relationship('r').node('b', 'PackagesImports').RETURN('a', 'b', 'r')
            
            self.pypherObject.Match.node('u', labels=self.extracted_entities).WHERE.u.property('name') == self.extracted_values
            query = str(self.pypherObject.RETURN.u)
            params = self.pypherObject.bound_params
            print ("\n ========== generated queries ===========")
            print (query)
            print (params)
            
            with self.driver.session() as  session:
                result = session.run(str(self.pypherObject), **dict(self.pypherObject.bound_params))

                # session.close()
                # result = session.run(str(p))
                print ("\n ========= result from neo4j ============ \n")
                query_result = result.data()

        # this does not include show all bundles condition
        elif self.extracted_intents == 'showDetailedBundleProjectInfo':

            self.pypherObject.Match.node('u', labels=self.extracted_entities).WHERE.u.property('name') == self.extracted_values
            query = str(self.pypherObject.RETURN.u)
            params = self.pypherObject.bound_params
            print ("\n ========== generated queries ===========")
            print (query)
            print (params)
            
            with self.driver.session() as  session:
                result = session.run(str(self.pypherObject), **dict(self.pypherObject.bound_params))

                print ("\n ========= result from neo4j ============ \n")
                query_result = result.data()

        # exports inside bundles
        elif self.extracted_intents == 'showExportsInBundle':


            print ("*********** show exports in bundle **************")
            print ("bundle slot value ", bundle_slot)
            self.pypherObject.Match.node('u', labels='bundles').relationship('r').node('b', labels='PackagesExports')
            query = str(self.pypherObject.RETURN('u','b', 'r'))
            params = self.pypherObject.bound_params
            print ("\n ========== generated queries ===========")
            print (query)
            print (params)
            # print(json.dumps(self.prediction, indent=2))
            
            with self.driver.session() as  session:
                result = session.run(str(self.pypherObject), **dict(self.pypherObject.bound_params))


                print ("\n ========= result from neo4j ============ \n")

                query_result = result.data()
                # print (query_result)


        else:
            print ("\n no Query written regarding this intention")
            print ("Intent is: \n ", self.extracted_intents)

        return [query, params, query_result]
    
if __name__ == '__main__':
    
    
    generateQuery = GenerateQuery(nlu_interpreter)
    generateQuery.predictIntentionAndEntity()

# sentence = "look for description of de.rcenvironment.components.excel.common.ExcelService service"
# sentence = "Bye"
# # sentence = "list packages.24 packages available in Car bundle"
# print ("Original sentence: \n", sentence)
# print ("--------------------------------------------")
# gQuery = GenerateQuery(train, sentence)
# gQuery.predictIntentionAndEntity()
# gQuery.convertTextToQuery()

## To do: Make code more shorter by creating function