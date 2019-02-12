import warnings
import ruamel.yaml as yaml
from pypher import __
from pypher.builder import Param, Pypher

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)


class GenerateQuery:

    def __init__(self, tracker):

        self.extracted_intents = dict()
        self.extracted_values = dict()
        self.pypher_object = Pypher()
        self.tracker = tracker

    def get_simple_query(self):
        extracted_intent = self.tracker.latest_message['intent']['name']

        if len(self.tracker.latest_message['entities']) > 0:
            extracted_value = self.tracker.latest_message['entities'][0]['value']
            extracted_entities = {
                self.tracker.latest_message['entities'][index]['entity']:
                    self.tracker.latest_message['entities'][index]['value']
                for index in range(len(self.tracker.latest_message['entities']))
            }
        else:
            extracted_entities = self.tracker.slots
        if len(extracted_entities) <= 0:
            return []

        if extracted_intent == 'showNodeInformation':
            if extracted_entities['node'] is None:
                return []
            self.pypher_object.Match.node('u').where.u.__name__.CONTAINS(Param('per_param', extracted_entities['node']))
            self.pypher_object.RETURN('u')

        elif extracted_intent == 'showAllNodes':
            self.pypher_object.Match.node('u', labels=self.get_key_with_none_empty_value(extracted_entities))
            self.pypher_object.RETURN('u')

        elif extracted_intent == 'countAllNodes':
            self.pypher_object.Match.node('u', labels=self.get_key_with_none_empty_value(extracted_entities))
            self.pypher_object.RETURN(__.count('u'))

        elif extracted_intent == 'showLargestCompilationUnit':

            if self.tracker.get_slot('Methods') is not None:

                self.pypher_object.Match.node('bundle', labels='bundles').relationship \
                    ('pkg', labels="Pkg_fragment").node('k').relationship \
                    ('kl', labels='compiled_By').node().relationship \
                    ('cp', labels="compiledUnits_topLevelType").node('n').relationship \
                    ('rl', 'Methods_Contains').node('mthd')

                self.pypher_object.RETURN('bundle.name', 'n.name', __.count('mthd'))
                self.pypher_object.OrderBy(__.count('mthd'))

            else:
                self.pypher_object.Match.node('bundle', labels='bundles').relationship \
                    ('pkg', labels="Pkg_fragment").node('k').relationship \
                    ('kl', labels='compiled_By').node('cmp')

                if self.tracker.get_slot('bundles') is not None:
                    self.pypher_object.WHERE(__.bundle.__name__ == self.tracker.get_slot('bundles'))

                self.pypher_object.RETURN('bundle.name', 'cmp.name', 'cmp.Loc')
                self.pypher_object.OrderBy(__.cmp.__Loc__)

            self.pypher_object.Desc()
            self.pypher_object.Limit(1)

        elif extracted_intent == 'showDetailInfoBundles':

            bundle_name = None
            key_value = None
            # iterate through all entities
            for key, value in self.tracker.slots.items():

                # key_value is assigned according to relation names
                if key == 'bundles':
                    bundle_name = value
                elif key == 'imports' or key == 'Exports':
                    key_value = value
                elif key == 'packages':
                    key_value = 'uses_pkgs'
                elif key == 'components':
                    key_value = 'uses_components'
                elif key == 'compilationUnit':
                    key_value = 'compiled_By'
                elif key == 'Methods':
                    key_value = 'Methods_Contains'

            # this is relation name
            if key_value == 'compiled_By':

                self.pypher_object.Match.node('u', labels='bundles').relationship \
                    ('f', labels="Pkg_fragment").node('n').relationship \
                    ('c', labels="compiled_By").node("m")

            elif key_value == 'Methods_Contains':
                self.pypher_object.Match.node('u', labels='bundles').relationship \
                    ('pkg', labels="Pkg_fragment").node('k').relationship \
                    ('kl', labels='compiled_By').node('n').relationship \
                    ('r', labels='compiledUnits_topLevelType').node('nl').relationship \
                    ('rl', labels='Methods_Contains').node('m')

            else:
                self.pypher_object.Match.node('u', labels='bundles').relationship \
                    ('r', labels=key_value).node('m')

            self.pypher_object.WHERE(__.u.__name__ == bundle_name)

            # this can be changed according to req. if we need all info or just names of packages
            # query = str(self.pypherObject.RETURN('u.name', 'm.name'))
            self.pypher_object.RETURN('u.name', 'm.name')

        elif self.extracted_intents == 'showProjectInformation':
            self.pypher_object.Match.node('u')
            self.pypher_object.WHERE(__.u.__name__ == self.tracker.get_slot('bundles'))
            self.pypher_object.RETURN('u')

        else:
            if extracted_value is not None:
                self.pypher_object.Match.node('u', labels=extracted_entities).WHERE.u.property(
                    'name') == extracted_value
                self.pypher_object.RETURN('u')

        query = str(self.pypher_object)
        params = self.pypher_object.bound_params
        return [query, params, extracted_intent]

    @staticmethod
    def get_key_with_none_empty_value(entities_dict):
        for key, value in entities_dict.items():
            print('key: ' + key)
            if value:
                print('value: ' + value)
                if key != "project":
                    return key
        return {}

    def convert_text_to_query(self):
        error = None
        [query, params, extracted_intent] = self.get_simple_query()

        if query is None or params is None or extracted_intent is None:
            error = "no Query written regarding this intention or intent prediction is not valid"

        return [query, params, self.tracker.latest_message['intent'], error]
