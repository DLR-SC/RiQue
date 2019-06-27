from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import logging
import json 
from rasa.core.agent import Agent
from rasa.core.policies.keras_policy import KerasPolicy
from rasa.core.policies.memoization import MemoizationPolicy
from rasa.nlu.model import Interpreter
import sys
import argparse

import warnings
import ruamel.yaml as yaml

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)

if __name__ == '__main__':

        parser = argparse.ArgumentParser(
            description='start chattting with bot')

        parser.add_argument('message')


        message = parser.parse_args().message
        # print ("message ", message)

        # message = sys.argv[1]
        # print ("message ", message)
        
        model_path = './models'
        nlu_interpreter = Interpreter.load(model_path + '/nlu/') 

        parsed_nlu_msg = nlu_interpreter.parse(message)
        print("Message", parsed_nlu_msg)
        '''
        print(json.dumps(parsed_nlu_msg, indent=2))
        
        # print ("NLU response ", nlu_interpreter.parse(msg))
        print ("---------------------- chat bot response ------------------------------")
        agent = Agent.load(model_path, interpreter = nlu_interpreter)

        print (agent.handle_text(message))
        '''
