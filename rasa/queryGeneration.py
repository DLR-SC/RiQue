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
        self.extracted_entities = None
        if len(self.prediction.get("entities")) > 0:
            # self.extracted_entities = None
            self.extracted_entities = self.prediction.get("entities")[0]['entity']
            self.extracted_values = self.prediction.get("entities")[0]['value']
            
        if len(self.prediction.get("entities")) > 1:
            self.extracted_entities = dict()
            self.extracted_entities = \
                {self.prediction.get("entities")[entity]['entity']: self.prediction.get("entities")[entity]['value'] 
                        for entity in range(len(self.prediction.get("entities")))}
            
        self.extracted_intents = self.prediction.get("intent")['name']

        # print ("Intent: ", self.extracted_intents)
        # print ("entity type: ", self.extracted_entities)
        # print ("entity value: ", self.extracted_values)
        # print ("=======================================")
        print(json.dumps(self.prediction, indent=2))

        return self.prediction
    
    def getSimpleQuery(self, extracted_entites, extracted_intent, extracted_value, query, query_result, params, bundle_slot=None):


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
            
        elif extracted_intent == 'showLargestCompilationUnit':
            self.pypherObject.Match.node('u', labels='bundles').relationship('pkg', labels="Pkg_fragment").node('k').relationship('kl', labels='compiled_By').node('m')

            if bundle_slot is not None:
                self.pypherObject.WHERE(__.u.__name__ == bundle_name)
            self.pypherObject.RETURN('u.name','m.Loc')
            self.pypherObject.OrderBy(__.m.__Loc__)
            self.pypherObject.Desc()
            self.pypherObject.Limit(1)

            query = str(self.pypherObject)
            params = self.pypherObject.bound_params

        elif extracted_intent == 'showDetailInfoBundles':

            # print ("extracted_entites ", self.extracted_entities)
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
                elif key == 'Methods':
                    key_value = 'Methods_Contains'

            # this is relation name
            if key_value == 'compiled_By':

                self.pypherObject.Match.node('u', labels='bundles').relationship('f', labels="Pkg_fragment").node('n').relationship('c', labels="compiled_By").node("m")
            
            elif key_value == 'Methods_Contains':
                self.pypherObject.Match.node('u', labels='bundles').relationship('pkg', labels="Pkg_fragment").node('k').relationship('kl', labels='compiled_By').node('n').relationship('r', labels = 'compiledUnits_topLevelType').node('nl').relationship('rl', labels = 'Methods_Contains').node('m')
                # query = str(self.pypherObject.RETURN('u', 'otherNodes'))
                # params = self.pypherObject.bound_params

            else:
                self.pypherObject.Match.node('u', labels='bundles').relationship('r', labels=key_value).node('m')

            self.pypherObject.WHERE(__.u.__name__ == bundle_name)

            # this can be changed according to req. if we need all info or just names of packages
            # query = str(self.pypherObject.RETURN('u.name', 'm.name'))

            query = str(self.pypherObject.RETURN('u.name','m.name'))
            params = self.pypherObject.bound_params

        elif self.extracted_intents == 'showProjectInformation':
            self.pypherObject.Match.node('u')
            self.pypherObject.WHERE(__.u.__name__ == bundle_slot)
            query = str(self.pypherObject.RETURN.u)
            params = self.pypherObject.bound_params

        else:
            self.pypherObject.Match.node('u', labels=extracted_entites).WHERE.u.property('name') == extracted_value
            query = str(self.pypherObject.RETURN.u)
            params = self.pypherObject.bound_params


        with self.driver.session() as session:
                result = session.run(str(self.pypherObject), **dict(params))

                # print ("\n ========= result from neo4j ============ \n")
                query_result = result.data()

        return [query, params, query_result]


    def convertTextToQuery(self, bundle_slot=None):


        query = None 
        query_result = None
        params = None

        print (" self.extracted_intents ", self.extracted_intents)
        
        [query, params, query_result] = self.getSimpleQuery(self.extracted_entities, self.extracted_intents, self.extracted_values, query, query_result, params, bundle_slot) 

        if query == None or params == None or query_result == None:
            print ("\n no Query written regarding this intention or intent prediction is not valid")      

        return [query, params, query_result]
    