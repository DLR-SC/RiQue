from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from response_builder import ResponseBuilder
import json

response_builder = ResponseBuilder()


class DisplayGeneralQuery(Action):

    def name(self):

        return "action_give_project_information"

    def run(self, dispatcher, tracker, domain):
        response = dict()
        if tracker.get_slot('project'):
            response = response_builder.get_query(tracker)
        else:
            response['error'] = "no project slot is filled inside action give project information action"
        dispatcher.utter_message(json.dumps(response))

        return []


class DisplayBundleDetailedQuery(Action):

    def name(self):

        return "action_show_detail_info_bundles"

    def run(self, dispatcher, tracker, domain):
        response = dict()
        if tracker.get_slot('bundles'):
            response = response_builder.get_query(tracker)
        else:
            response['error'] = "no bundles slot filled inside show detailed bundle project info"
        dispatcher.utter_message(json.dumps(response))

        return []


'''
Get compilation units with highest number of code lines
'''


class DisplayLargestCompilationUnit(Action):

    def name(self):

        return "action_show_largest_compilationUnit"

    def run(self, dispatcher, tracker, domain):
        response = response_builder.get_query(tracker)
        dispatcher.utter_message(json.dumps(response))
        return []


'''
Show specific node information
'''


class ShowNodeInformation(Action):

    def name(self):

        return "action_show_node_information"

    def run(self, dispatcher, tracker, domain):
        response = dict()
        if tracker.get_slot('node'):
            response = response_builder.get_query(tracker)
        else:
            response['error'] = "no node slot filled inside action show node information"
        dispatcher.utter_message(json.dumps(response))

        return []


'''
show nodes
'''


class ShowAllNodes(Action):

    def name(self):

        return "action_show_all_nodes"

    def run(self, dispatcher, tracker, domain):
        response = response_builder.get_query(tracker)
        dispatcher.utter_message(json.dumps(response))
        return []


'''
count all nodes
'''


class CountAllNodes(Action):

    def name(self):

        return "action_count_all_nodes"

    def run(self, dispatcher, tracker, domain):
        response = response_builder.get_query(tracker)
        dispatcher.utter_message(json.dumps(response))
        return []

