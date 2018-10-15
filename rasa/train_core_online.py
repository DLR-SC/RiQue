from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import argparse
from rasa_core.agent import Agent
from rasa_core.channels import console
from rasa_core.utils import EndpointConfig
# from rasa_core 
from rasa_core.train import online
from rasa_core.interpreter import RegexInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter

logger = logging.getLogger(__name__)


# def run_model_online(interpreter,
#                           domain_file="domain.yml",
#                           training_data_file='stories.md'):
#     agent = Agent(domain_file,
#                   policies=[MemoizationPolicy(), KerasPolicy()],
#                   interpreter=interpreter)
#     data = agent.load_data(training_data_file)
#         # agent.train(data)

#     agent.train(
#       data,
#       augmentation_factor = 50,
#       epochs = 50,
#       batch_size = 10,
#       validation_split = 0.2)
      

    
#     # agent.train_online(training_data_file,
#     #                    input_channel=input_channel,
#     #                    max_history=2,
#     #                    batch_size=50,
#     #                    epochs=200,
#     #                    max_training_samples=300)

#     return agent


if __name__ == '__main__':

    logging.basicConfig(level="INFO")
    nlu_interpreter = RasaNLUInterpreter('./projects/default/default/Neo4jNlu')

    # run_model_online(nlu_interpreter)

    
    # interpreter = NaturalLanguageInterpreter.create("models/nlu/current")

    action_endpoint = EndpointConfig(url="http://localhost:5056/webhook")

    agent = Agent.load("./models/dialog/", interpreter=nlu_interpreter, action_endpoint=action_endpoint)
    online.serve_agent(agent)