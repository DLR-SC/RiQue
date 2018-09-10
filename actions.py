from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse

from rasa_core import utils
from rasa_core.actions import Action
from rasa_core.interpreter import RasaNLUInterpreter

class GraphDBRequester(object):
    def search(self, info):
        return "papi's pizza place"


class ActionQueryBundlesWithMostImports(Action):
    def name(self):
        return 'action_query_bundles_with_most_imports'

    def run(self, dispatcher, tracker, domain):
        response = urllib.request.urlopen("https://api.github.com/users/pseipel/orgs").read()
        dispatcher.utter_message("here is what I found for imports: " + response)
        return []

		
class ActionQueryBundlesWithMostExports(Action):
    def name(self):
        return 'action_query_bundles_with_most_exports'

    def run(self, dispatcher, tracker, domain):
        response = urllib.request.urlopen("https://api.github.com/users/pseipel/orgs").read()
        dispatcher.utter_message("here is what I found for exports: " + response)
        return []
