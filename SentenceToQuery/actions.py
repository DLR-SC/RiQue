from rasa_sdk import Action
from query_generator import GenerateQuery
import json
from py2neo import Graph

def get_nlg(graph_query):
    graph = Graph(auth=("neo4j","sss"))
    graph_response = graph.evaluate(graph_query)
    return graph_response

# Actions for new intents
class GetBiggestComponent(Action):
    def name(self):
        return "action_get_biggest_component"

    def run(self, dispatcher, tracker, domain):
        query = None
        intent = tracker.latest_message['intent']
        child_comp = tracker.get_slot('component_type_child')
        parent_comp = tracker.get_slot('component_type_parent')
        error = None
        query = GenerateQuery.get_biggest_component(child_comp, parent_comp)
        response = ResponseBuilderUtils.build_response(query, intent, error)
        graph_response = get_nlg(response['query'])
        graph_response['intent']=intent
        full_response = {'name':graph_response, 'intent':intent}
        dispatcher.utter_message(json.dumps(graph_response))
        return []

class GetSmallestComponent(Action):
    def name(self):
        return "action_get_smallest_component"

    def run(self, dispatcher, tracker, domain):
        query = None
        intent = tracker.latest_message['intent']
        entity = tracker.latest_message['entities']
        comp = entity[0]['value']
        error = None
        query = GenerateQuery.get_smallest_component(comp)
        response = ResponseBuilderUtils.build_response(query, intent, error)
        graph_response = get_nlg(response['query'])
        full_response = {'data':graph_response, 'intent':graph_response['name']}
        dispatcher.utter_message(json.dumps(graph_response['name']))
        return []

class Greet(Action):
    def name(self):
        return "action_greet"

    def run (self, dispatcher, tracker, domain):
        response = ""

# Old actions
class DisplayGeneralQuery(Action):

    def name(self):

        return "action_give_project_information"

    def run(self, dispatcher, tracker, domain):
        query = None
        intent = tracker.latest_message['intent']
        error = None
        if tracker.get_slot('project'):
            query = GenerateQuery.get_project_information(tracker.get_slot('project'))
        else:
            error = "no project slot is filled inside action give project information action"
        response = ResponseBuilderUtils.build_response(query, intent, error)
        dispatcher.utter_message(json.dumps(response))
        return []


class DisplayBundleDetailedQuery(Action):

    def name(self):

        return "action_show_detail_info_bundles"

    def run(self, dispatcher, tracker, domain):
        query = None
        intent = tracker.latest_message['intent']
        error = None
        if tracker.get_slot('bundle'):
            query_aspect = tracker.get_slot('nodeType')
            query = GenerateQuery.get_detailed_bundle_info_query(tracker.get_slot('bundle'), query_aspect)
        else:
            error = "no bundles slot filled inside show detailed bundle project info"
        response = ResponseBuilderUtils.build_response(query, intent, error)
        dispatcher.utter_message(json.dumps(response))

        return []


'''
Get compilation units with highest number of code lines
'''


class DisplayLargestCompilationUnit(Action):

    def name(self):

        return "action_show_largest_compilationUnit"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message['intent']
        bundle_name = tracker.get_slot('bundle')
        order = tracker.get_slot('nodeType')
        query = GenerateQuery.get_largest_compilation_unit_query(bundle_name, order)
        response = ResponseBuilderUtils.build_response(query, intent)
        dispatcher.utter_message(json.dumps(response))
        return []


'''
Show specific node information
'''


class ShowNodeInformation(Action):

    def name(self):

        return "action_show_node_information"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message['intent']
        query = None
        error = None
        if tracker.get_slot('node'):
            query = GenerateQuery.get_node_information_query(tracker.get_slot('node'))
        elif tracker.get_slot('bundle'):
            print("bundle:" + tracker.get_slot('bundle'))
            query = GenerateQuery.get_node_information_query(tracker.get_slot('bundle'), 'bundles')
        elif tracker.get_slot('compilationUnit'):
            print("compilationunit:" + tracker.get_slot('compilationUnit'))
            query = GenerateQuery.get_node_information_query(tracker.get_slot('compilationUnit'), 'compilationUnit')
        else:
            error = "no node slot filled inside action show node information"
        response = ResponseBuilderUtils.build_response(query, intent, error)
        dispatcher.utter_message(json.dumps(response))
        return []


'''
show nodes
'''


class ShowAllNodes(Action):

    def name(self):

        return "action_show_all_nodes"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message['intent']
        if tracker.get_slot('nodeType'):
            query = GenerateQuery.get_show_all_nodes_query(tracker.get_slot('nodeType'))
        else:
            query = GenerateQuery.get_show_all_nodes_query()
        response = ResponseBuilderUtils.build_response(query, intent)
        dispatcher.utter_message(json.dumps(response))
        return []


'''
count all nodes
'''


class count_components(Action):

    def name(self):

        return "action_count_all_nodes"

    def run(self, dispatcher, tracker, domain):
        query = None
        intent = tracker.latest_message['intent']
        entity = tracker.latest_message['entities']
        parent_comp = tracker.get_slot('component_type_parent')
        # entity[0] gives the output and ['value'] gives the entity value
        child_comp = entity[0]['value']
        error = None
        query = GenerateQuery.get_count_all_nodes_query(child_comp, parent_comp)
        graph_response = get_nlg(query)
        response = ResponseBuilderUtils.build_response(graph_response, intent, error)
        dispatcher.utter_message(json.dumps(response))
        return []

class ResponseBuilderUtils:

    @staticmethod
    def build_response(query, intent, error=None):
        response = dict()
        if error:
            response['error'] = error
        response['query'] = query
        response['intent'] = intent
        return response

