from py2neo import Graph
"""
    def __init__:
        graph = Graph(auth=("neo4j","sss"))
"""
 
class Graph2NLG:
    def get_nlg(graph_query):
        graph = Graph(auth=("neo4j","sss"))
        graph_response = graph.evaluate(graph_query)
        return graph_response

