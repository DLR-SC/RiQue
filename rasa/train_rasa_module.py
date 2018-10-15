# from __future__ import absolute_import
# from __future__ import division
# from __future__ import unicode_literals

import logging

from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter

import argparse

from train_nlu import trainNluModel

import warnings
import ruamel.yaml as yaml

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)

class TrainBot:

	def __init__(self):

		self.training_data_nlu = "./nlu.json"
		self.conf_path_nlu = "./nlu_config.yml"
		self.training_data_core = './stories.md'
		self.model_path_core = './models/dialogue'
		self.model_path_nlu = './projects/default/default/Neo4jNlu'

if __name__ == '__main__':
	
	trainbot = TrainBot()

	logging.basicConfig(level='INFO')


	parser = argparse.ArgumentParser(
            description='starts the bot training')

	parser.add_argument('task', choices=["train-nlu", "train-dialogue", "train-all"], help="what the bot should do?")

	task = parser.parse_args().task
	print ("task chosen ", task)


	if task == 'train-nlu':

		print ("----- training nlu only ")
		train = trainNluModel(trainbot.training_data_nlu, trainbot.conf_path_nlu)
		train.startTraining()

	if task == 'train-dialogue':

		print ("----- training core only ")
		

		agent = Agent('domain.yml', policies = [MemoizationPolicy(), KerasPolicy()])

		data = agent.load_data(trainbot.training_data_core)

		agent.train(
				data,
				augmentation_factor = 50,
				epochs = 45,
				batch_size = 10,
				validation_split = 0.2)
				
		agent.persist(trainbot.model_path_core)

		
		nlu_interpreter = RasaNLUInterpreter(trainbot.model_path_nlu) 

		agent = Agent.load(trainbot.model_path_core, interpreter = nlu_interpreter)
		print ("inside train dialogue")

	if task == 'train-all':

		print ("---- training nlu and core ----")

		train = trainNluModel(trainbot.training_data_nlu, trainbot.conf_path_nlu)
		train.startTraining()

		agent = Agent('domain.yml', policies = [MemoizationPolicy(), KerasPolicy()])

		data = agent.load_data(trainbot.training_data_core)

		agent.train(
				data,
				augmentation_factor = 50,
				epochs = 45,
				batch_size = 10,
				validation_split = 0.2)
				
		agent.persist(trainbot.model_path_core)
		nlu_interpreter = RasaNLUInterpreter(trainbot.model_path_nlu)
		agent = Agent.load(trainbot.model_path_core, interpreter = nlu_interpreter)
