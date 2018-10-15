from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import logging
import json 
from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
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
	
	model_path = './models/dialogue'
	nlu_interpreter = RasaNLUInterpreter('./projects/default/default/Neo4jNlu') 

	parsed_nlu_msg = nlu_interpreter.interpreter.parse(message)
	print(json.dumps(parsed_nlu_msg, indent=2))
	
	# print ("NLU response ", nlu_interpreter.parse(msg))
	print ("---------------------- chat bot response ------------------------------")
	agent = Agent.load(model_path, interpreter = nlu_interpreter)

	print (agent.handle_text(message))