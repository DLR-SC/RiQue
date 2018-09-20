from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
import urllib

class ActionQueryBundlesWithMostImports(Action):
    def name(self):
        return "action_query_bundles_with_most"

    def run(self, dispatcher, tracker, domain):
        # response = urllib.request.urlopen("https://api.github.com/users/pseipel/orgs").read()
        queryEntity = tracker.get_slot("graph_db_query")
        if tracker.get_slot("graph_db_query") == "exports":
            queryString = "MATCH (b:Bundle)-[c:CONTAINS]->(manifest:Manifest),(manifest).[:DECLARES]->(manifestSection), " \
                          "(manifestSection)-[:HAS]->(me:ManifestEntry) RETURN b, count(me.mame = \"Export-Package\") " \
                          "as Exports ORDER BY Exports DESC Limit 1"
            dispatcher.utter_message(queryString)
        else:
            dispatcher.utter_message("I still have to learn the query for this entity: " + queryEntity)
        return []