import logging
import argparse
import warnings
import ruamel.yaml as yaml

import rasa_core
from rasa_core.utils import EndpointConfig
from rasa_core.run import serve_application
from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter

from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)

class TrainBot:

    def __init__(self):
        self.training_data_nlu = "./training_dataset.json"
        self.conf_path_nlu = "./nlu_config.yml"
        self.training_data_core = './stories.md'
        self.model_path_core = './models/dialogue'
        self.model_path_nlu = './projects/default/default/Neo4jNlu'

    def train_nlu(self):
        data = load_data(self.training_data_nlu)
        nlu_trainer = Trainer(config.load(self.conf_path_nlu))
        nlu_trainer.train(data) 
        nlu_trainer.persist('./projects/default/',  fixed_model_name = 'Neo4jNlu')

        #train = trainNluModel(self., self.conf_path_nlu)
        #train.startTraining()

    def train_core(self):
        agent = Agent('domain.yml', policies = [MemoizationPolicy(max_history=3), KerasPolicy(max_history=3, epochs=40, batch_size=10)])
        data = agent.load_data(self.training_data_core)
       
        agent.train(data, augmentation_factor = 50, validation_split = 0.2)
        agent.persist(self.model_path_core)
        
    def run_bot(self):
        nlu_interpreter = RasaNLUInterpreter(self.model_path_nlu)
        endpt = EndpointConfig(url="http://localhost:5055/webhook")
        agent = Agent.load(self.model_path_core, interpreter = nlu_interpreter, action_endpoint=endpt)
        rasa_core.run.serve_application(agent, channel='cmdline') 


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description='starts the bot training')
    parser.add_argument('task', choices=["train-nlu", "train-dialogue", "train-all", "bot"], help="what the bot should do?")
    task = parser.parse_args().task

    trainer = TrainBot()

    if task == 'train-nlu':
        logger.info("================ Training Rasa NLU ================ " )
        trainer.train_nlu()

    if task == 'train-dialogue':
        logger.info("================ Training Rasa Core ================ " )
        trainer.train_core()

    if task == 'train-all':
        logger.info("================ Training Rasa NLU & Core ================ " )
        trainer.train_nlu()
        trainer.train_core()

    if task == 'bot':
        logger.info("================ Firing up the Chatbot ================ " )
        trainer.run_bot()
