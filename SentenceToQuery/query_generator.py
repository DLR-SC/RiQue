import warnings
import ruamel.yaml as yaml
from pypher import __
from pypher.builder import Param, Pypher

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)


class GenerateQuery:
    @staticmethod
    def reformat_query(pypher_object):
        query = str(pypher_object)
        for key, value in pypher_object.bound_params.items():
            if key in query:
                # because key present in param does not have $ sign
                modified_key = "$" + key
                query = query.replace(modified_key, '"' + str(value) + '"')
        return query

    @staticmethod
    def get_biggest_component(child_comp, parent_comp):
        """
        :param child_comp: children component name
        :param parent_comp: parent component name
        :return: Biggest children component present in parent component
        """
        cy_query = u'MATCH (b:Bundle)-[r:REQUIRES|CONTAINS]->(c) WITH b, COUNT(c) as child RETURN b ORDER BY child DESC LIMIT 1'
        return cy_query

    @staticmethod
    def get_smallest_component(comp):
        """
        :param comp: component name
        :return: Biggest children component present in parent component
        """
        cy_query = u'MATCH (b:Bundle)-[r:REQUIRES|CONTAINS]->(c) WITH b, COUNT(c) as child RETURN b ORDER BY child LIMIT 1'
        return cy_query


    @staticmethod
    def get_node_information_query(node_name, node_type=None):
        """
        :param node_name: name of the node to get information about.
        :return: the query for showing general information of one node (any entity) with a specific name.
        """
        pypher_object = Pypher()
        if node_type is None:
            pypher_object.Match.node('u').where.u.__name__.CONTAINS(Param('per_param', node_name))
        else:
            pypher_object.Match.node('u', labels=node_type).where.u.__name__.CONTAINS(Param('per_param', node_name))
        pypher_object.RETURN('u')
        return GenerateQuery.reformat_query(pypher_object)

    @staticmethod
    def get_show_all_nodes_query(node_type=None):
        """
        :param node_type: type of nodes to show.
        :return: the query to show all nodes. Optional: Type of nodes to be recognized.
        """
        # should be bundle, copilationUnit or package. Could be extracted via tracker.slots.get('nodeType').
        pypher_object = Pypher()
        if node_type is None:
            pypher_object.Match.node('u')
        else:
            pypher_object.Match.node('u', labels=node_type)
        pypher_object.RETURN('u')
        return GenerateQuery.reformat_query(pypher_object)

    @staticmethod
    def get_count_all_nodes_query(child_comp, parent_comp):
        """
        :param node_type: type of nodes to count.
        :return: the query to count all nodes. Optional counts nodes of a type.
        """
        notation = {'bundles':u'Bundle', 'islands':u'Bundle', 'packages':U'Package','compilation units':u'Class','components':u'ServiceComponent','classes':u'Class'}
        node = notation[child_comp]
        cy_query = u'MATCH (:'+ node +') RETURN COUNT(*)'
        return cy_query

    @staticmethod
    def get_largest_compilation_unit_query(bundle_name=None, order="mthd"):
        """
        :param bundle_name: in entire project or in one specific bundle. Default is in all bundles.
        :param order: largest by lines of code (loc) or number of methods (mthd). Default is "mthd".
        :return: the query for the largest compilation unit.
        'large' in this context means lines of code or number of methods.
        It also can be the largest CU in a bundle or in general.

        """
        pypher_object = Pypher()
        if order == "loc":
            pypher_object.Match.node('bundle', labels='bundles')\
                .relationship('pkg', labels="Pkg_fragment").node('k')\
                .relationship('kl', labels='compiled_By').node('cmp')
            if bundle_name:
                pypher_object.WHERE(__.bundle.__name__ == bundle_name)
            pypher_object.RETURN('cmp')
            pypher_object.OrderBy(__.cmp.__Loc__)
        return GenerateQuery.reformat_query(pypher_object)

    @staticmethod
    def get_detailed_bundle_info_query(bundle_name, aspect=None):
        """
        :param bundle_name: retrieve specific information for this bundle.
        :param aspect: should be 'bundles', 'imports', 'Exports', 'packages','components','compilationUnit','Methods'.
        :return: the query for (general or specific) information about one bundle.
        """
        if aspect is None:
            return GenerateQuery.get_node_information_query(bundle_name, 'bundles')

        pypher_object = Pypher()
        if aspect == 'compilationUnit':
            pypher_object.Match.node('u', labels='bundles').relationship('f', labels="Pkg_fragment").node('n')\
                .relationship('c', labels="compiled_By").node("m")

        elif aspect == 'methods':
            pypher_object.Match.node('u', labels='bundles').relationship('pkg', labels="Pkg_fragment").node('k')\
                .relationship('kl', labels='compiled_By').node('n')\
                .relationship('r', labels='compiledUnits_topLevelType').node('nl')\
                .relationship('rl', labels='Methods_Contains').node('m')

        else:
            if aspect == 'packages':
                labels = 'uses_pkgs'
            elif aspect == 'components':
                labels = 'uses_components'
            else:
                labels = aspect

            pypher_object.Match.node('u', labels='bundles').relationship('r', labels=labels).node('m')

        pypher_object.Match.node('u').where.u.__name__.CONTAINS(Param('per_param', bundle_name))

        # this can be changed according to req. if we need all info or just names of packages
        # query = str(self.pypherObject.RETURN('u.name', 'm.name'))
        pypher_object.RETURN('u.name', 'm.name')
        return GenerateQuery.reformat_query(pypher_object)

    @staticmethod
    def get_project_information(project_name):
        """
        :param project_name: the name of the current project.
        :return: the query for general information about the current project.
        """
        pypher_object = Pypher()
        pypher_object.Match.node('u')
        pypher_object.WHERE(__.u.__name__ == project_name)
        pypher_object.RETURN('u')
        return GenerateQuery.reformat_query(pypher_object)
