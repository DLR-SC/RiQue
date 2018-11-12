import rasa_nlu
from rasa_nlu.model import Interpreter
from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config

import warnings
import ruamel.yaml as yaml

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)

class trainNluModel:
    
    def __init__(self, train_data_path, config_path):
        
        self.train_data_path = train_data_path
        self.config_path = config_path
        self.model_directory = None
        
    def startTraining(self):
        
        print ("training")
        training_data = load_data(self.train_data_path)
        trainer = Trainer(config.load(self.config_path))
        trainer.train(training_data)       
        self.model_directory = trainer.persist('./projects/default/',  fixed_model_name = 'Neo4jNlu')

# if __name__ == '__main__':

#     training_data = "./nlu.json"
#     conf_path = "./nlu_config.yml"
#     train = trainNluModel(training_data, conf_path)
#     # #start training
#     train.startTraining()