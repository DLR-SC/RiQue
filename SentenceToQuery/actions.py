from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from response_builder import ResponseBuilder
import json

response_builder = ResponseBuilder()


class DisplayGeneralQuery(Action):

    def name(self):

        return "action_give_project_information"

    def run(self, dispatcher, tracker, domain):
        if tracker.get_slot('project'):
            response_builder.get_query(dispatcher, tracker)
        else:
            response = dict()
            response['error'] = "no project slot is filled inside action give project information action"
            dispatcher.utter_custom_message(response)

        return []


class DisplayBundleDetailedQuery(Action):

    def name(self):

        return "action_show_detail_info_bundles"

    def run(self, dispatcher, tracker, domain):
        if tracker.get_slot('bundles'):
            response_builder.get_query(dispatcher, tracker)
        else:
            response = dict()
            response['error'] = "no bundles slot filled inside show detailed bundle project info"
            dispatcher.utter_custom_message(response)

        return []


'''
Get compilation units with highest number of code lines
'''


class DisplayLargestCompilationUnit(Action):

    def name(self):

        return "action_show_largest_compilationUnit"

    def run(self, dispatcher, tracker, domain):
        if tracker.get_slot('compilationUnit'):
            response_builder.get_query(dispatcher, tracker)

        else:
            dispatcher.utter_message(json.dumps({'error': "compilationUnit slot is not filled"}))

        return []


'''
Show specific node information
'''


class ShowNodeInformation(Action):

    def name(self):

        return "action_show_node_information"

    def run(self, dispatcher, tracker, domain):
        if tracker.get_slot('node'):
            response_builder.get_query(dispatcher, tracker)
        else:
            dispatcher.utter_message(json.dumps({'error': "no node slot filled inside action show node information"}))

        return []


'''
show nodes
'''


class ShowAllNodes(Action):

    def name(self):

        return "action_show_all_nodes"

    def run(self, dispatcher, tracker, domain):
        response_builder.get_query(dispatcher, tracker)

        return []


'''
count all nodes
'''


class CountAllNodes(Action):

    def name(self):

        return "action_count_all_nodes"

    def run(self, dispatcher, tracker, domain):
        recent_message = tracker.latest_message['text']
        if tracker.get_slot('packages') | \
                tracker.get_slot('bundles') | \
                tracker.get_slot('services') | \
                tracker.get_slot('compilationUnit') | \
                tracker.get_slot('Methods'):
            response_builder.get_query(recent_message, dispatcher)
        else:
            response = dict()
            response['error'] = "no slot filled count all nodes"
            dispatcher.utter_message(response)

        return []

