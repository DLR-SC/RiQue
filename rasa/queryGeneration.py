import pypher

from pypher import __
from pypher.builder import Param, Pypher
from neo4j.v1 import GraphDatabase
from train_rasa_module import TrainBot
from rasa_core.interpreter import RasaNLUInterpreter

import json 

class GenerateQuery:
    
    def __init__(self, sentence):
        
        # self.interpret = Interpreter.load(train.model_directory)
        self.trainedBot = TrainBot()
        self.interpret = RasaNLUInterpreter(self.trainedBot.model_path_nlu)

        # self.interpret = interpreter
        self.extracted_intents = None
        
        self.extracted_values = None # entities values
        self.prediction = None
        self.pypherObject = Pypher()
        self.uri = "bolt://localhost:7687"
        self.driver = GraphDatabase.driver(self.uri, auth=("neo4j", "123456"))
        self.sentence = sentence
        
    def predictIntentionAndEntity(self):
        

        self.prediction = self.interpret.parse(self.sentence)
        print ("length of entities ", len(self.prediction.get("entities")))
        
        if len(self.prediction.get("entities")) > 0:
            self.extracted_entities = None
            self.extracted_entities = self.prediction.get("entities")[0]['entity']
            self.extracted_values = self.prediction.get("entities")[0]['value']
            
        if len(self.prediction.get("entities")) > 1:
            self.extracted_entities = dict()
            self.extracted_entities = \
                {self.prediction.get("entities")[entity]['entity']: self.prediction.get("entities")[entity]['value'] 
                        for entity in range(len(self.prediction.get("entities")))}
            
        self.extracted_intents = self.prediction.get("intent")['name']

        print ("Intent: ", self.extracted_intents)
        print ("entity type: ", self.extracted_entities)
        print ("entity value: ", self.extracted_values)
        print ("=======================================")
        print(json.dumps(self.prediction, indent=2))

        return self.prediction
    
    def getSimpleQuery(self, extracted_entites, extracted_intent, extracted_value, query, query_result, params):


        # self.pypherObject.Match.node('u', labels=extracted_intent).WHERE.u.property('name') == extracted_value
        if extracted_intent == 'showNodeInformation':
            self.pypherObject.Match.node('u').where.u.__name__.CONTAINS(Param('per_param', extracted_value))
            query = str(self.pypherObject.RETURN.u)
            params = self.pypherObject.bound_params


        elif extracted_intent == 'showAllNodes':
            self.pypherObject.Match.node('u', labels=extracted_entites)
            query = str(self.pypherObject.RETURN.u)
            params = self.pypherObject.bound_params

        elif extracted_intent == 'countAllNodes':
            self.pypherObject.Match.node('u', labels=extracted_entites)
            # self.pypherObject.Match.node('u', labels=extracted_entites).where.u.__name__.COUNT(Param('per_param', 'u'))


            self.pypherObject.RETURN(__.count('u'))
            query = str(self.pypherObject)
            params = self.pypherObject.bound_params
            
        elif extracted_intent == 'showDetailInfoBundles':

            print ("extracted_entites ", self.extracted_entities)
            bundle_name = None
            key_value = None
            for key, value in self.extracted_entities.items():

                if key == 'BundlesName':
                    bundle_name = value
                elif key == 'Imports' or key == 'Exports':
                    key_value = value
                elif key == 'packages':
                    key_value = 'uses_pkgs'
                elif key == 'components':
                    key_value = 'uses_components'
                elif key == 'compilationUnit':
                    key_value = 'compiled_By'

            if key_value == 'compiled_By':
                self.pypherObject.Match.node('u', labels='bundles').relationship('f', labels="Pkg_fragment").node('n').relationship('c', labels="compiled_By").node("m")

            else:
                self.pypherObject.Match.node('u', labels='bundles').relationship('r', labels=key_value).node('m')

            self.pypherObject.WHERE(__.u.__name__ == bundle_name)
            query = str(self.pypherObject.RETURN('u', 'm'))
            params = self.pypherObject.bound_params

        else:
            self.pypherObject.Match.node('u', labels=extracted_entites).WHERE.u.property('name') == extracted_value
            query = str(self.pypherObject.RETURN.u)
            params = self.pypherObject.bound_params


        with self.driver.session() as session:
                result = session.run(str(self.pypherObject), **dict(params))

                print ("\n ========= result from neo4j ============ \n")
                query_result = result.data()

        return [query, params, query_result]


    def convertTextToQuery(self, bundle_slot=None):


        query = None 
        query_result = None
        params = None

        print (" self.extracted_intents ", self.extracted_intents)
        
        if self.extracted_intents == 'showProjectInformation':
            
            [query, params, query_result] = self.getSimpleQuery(self.extracted_entities, self.extracted_intents, self.extracted_values, query, query_result, params)
            

        # this does not include show all bundles condition
        elif self.extracted_intents == 'showDetailInfoBundles':
            [query, params, query_result] = self.getSimpleQuery(self.extracted_entities, self.extracted_intents, self.extracted_values, query, query_result, params)


        # show specific node information
        elif self.extracted_intents == 'showNodeInformation':

            [query, params, query_result] = self.getSimpleQuery(self.extracted_entities, self.extracted_intents, self.extracted_values, query, query_result, params)
  
        # show all nodes such as packages/bundles
        elif self.extracted_intents =='showAllNodes':

            [query, params, query_result] = self.getSimpleQuery(self.extracted_entities, self.extracted_intents, self.extracted_values, query, query_result, params)
             
        # count all nodes such as packages/bundles
        elif self.extracted_intents == 'countAllNodes':

            [query, params, query_result] = self.getSimpleQuery(self.extracted_entities, self.extracted_intents, self.extracted_values, query, query_result, params)


        # exports inside bundles
        elif self.extracted_intents == 'showExportsInBundle':

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


        else:
            print ("\n no Query written regarding this intention")
            print ("Intent is: \n ", self.extracted_intents)

        return [query, params, query_result]
    