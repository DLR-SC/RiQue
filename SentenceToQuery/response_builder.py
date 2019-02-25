from query_generator import GenerateQuery
import json


class ResponseBuilder:

    @staticmethod
    def get_query(tracker):
        response = dict()
        g_query = GenerateQuery(tracker)
        [query, params, extracted_intent, error] = g_query.convert_text_to_query()
        if error is not None:
            response['error'] = error

        if params is not None:
            # # restructure query
            for key, value in params.items():
                if key in query:
                    # because key present in param does nto have $ sign
                    modified_key = "$" + key
                    query = query.replace(modified_key, '"' + str(value) + '"')
            response['query'] = query
            response['intent'] = extracted_intent
        return response

    @staticmethod
    def standardize_intent_names(self):
        intents = {'greet': 'Greet', 'goodbye': 'Good Bye', 'showProjectInformation': 'Show project information',
                   'showNodeInformation': 'Show node information', 'showAllNodes': 'Show all nodes',
                   'my_name_is': 'Greet with name', 'countAllNodes': 'Count all nodes',
                   'showDetailInfoBundles': 'Show information about specific bundle',
                   'showLargestCompilationUnit': 'Show largest compilation unit'}

        return intents
