from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
import pypher
from pypher import Pypher, __
from pypher.builder import Param
from queryGeneration import GenerateQuery
from rasa_core.events import AllSlotsReset, Restarted

class ActionCheckRestaurants(Action):

    def name(self):
      # type: () -> Text
      return "action_check_restaurants"

    def run(self, dispatcher, tracker, domain):
      # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]

      info = tracker.get_slot('GPE')
      dispatcher.utter_message(info)
      # info2 = tracker.get_slot('restaurant')
      # dispatcher.utter_message(info2)

      result = None
      
      # self.recent_message = (tracker.latest_message)['text']
      # dispatcher.utter_message(self.recent_message)
      
      dispatcher.utter_message(" ==== current state of tracker ======")
      
      # dispatcher.utter_message(tracker.current_state())


      # message = tracker.latest.text 
      # operate on(message)

      if tracker.get_slot('GPE'):


          with open('restaurants.txt') as file:
            data = file.read()
            dispatcher.utter_message("list of restaurants in tracker.get_slot('city')")
            dispatcher.utter_message(data)

          dispatcher.utter_message("action_check_restaurants being called ..")

      else:
          dispatcher.utter_message("no GPE slot filled inside action check restaurant")
          
      # cuisine = tracker.get_slot('cuisine')
      # q = "select * from restaurants where cuisine='{0}' limit 1".format(cuisine)
      # result = db.query(q)

      # return [SlotSet("matches", result if result is not None else [])]

      return []
      

class showDetailedRestaurantInfo(Action):


    def name(self):
      # type: () -> Text
      return "action_show_detailed_restaurant_info"

    def run(self, dispatcher, tracker, domain):
      # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]

      info = tracker.get_slot('GPE')
      dispatcher.utter_message('City name: ')
      dispatcher.utter_message(info)
      info2 = tracker.get_slot('restaurant')
      dispatcher.utter_message('restaurant name: ')
      dispatcher.utter_message(info2)


      result = None
      
      # self.recent_message = (tracker.latest_message)['text']
      # dispatcher.utter_message(self.recent_message)
            
      # dispatcher.utter_message(tracker.current_state())

      # message = tracker.latest.text 
      # operate on(message)

      if tracker.get_slot('restaurant'):

          result = "restaurant slot found"
          dispatcher.utter_message(" It is located near HBF. ")

      else:
          dispatcher.utter_message("no restaurant in particular city slot being called")



      return []

class DisplayGeneralQuery(Action):


    def name(self):

      return "action_give_project_information"

    def run(self, dispatcher, tracker, domain):
      # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]

    # tracker.get_slot('city')[bool(tracker.get_slot('city'))] 
      dispatcher.utter_message("action give project info being called ")

      recent_message = (tracker.latest_message)['text']

      dispatcher.utter_message(" ==== current state of tracker ======")
      # dispatcher.utter_message(tracker.current_state)

      result = None
      failure = None
      if tracker.get_slot('project'):

          displayQueryOutput(recent_message, dispatcher)
          # gQuery = GenerateQuery(recent_message)
          # parse_msg = gQuery.predictIntentionAndEntity()
          
          # [query, params, result] = gQuery.convertTextToQuery()
          # dispatcher.utter_message("===== Query =====")
          # dispatcher.utter_message(query)
          # dispatcher.utter_message("=== query params =====")
          # dispatcher.utter_message(str(params))
          # dispatcher.utter_message("===== result =====")
          # dispatcher.utter_message(str(result))

          # print ("parse msg")

          # result = "project info show bitte"
          dispatcher.utter_message("project info being uttered ..")

      else:
          
          dispatcher.utter_message("no project slot is filled inside action give project information action")

      return []


class DisplayBundleQuery(Action):


    def name(self):

      return "action_show_detailed_bundle_project_info"

    def run(self, dispatcher, tracker, domain):
      # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]

    # tracker.get_slot('city')[bool(tracker.get_slot('city'))] 
      dispatcher.utter_message("action give **detailed** project info being called ")

      recent_message = (tracker.latest_message)['text']

      # dispatcher.utter_message(tracker.current_state)

      result = None
      failure = None

      if tracker.get_slot('bundles'):

          displayQueryOutput(recent_message, dispatcher)
          # gQuery = GenerateQuery(recent_message)
          # parse_msg = gQuery.predictIntentionAndEntity()
          
          # [query, params, result] = gQuery.convertTextToQuery()
          # dispatcher.utter_message("===== Query =====")
          # dispatcher.utter_message(query)
          # dispatcher.utter_message("=== query params =====")
          # dispatcher.utter_message(str(params))
          # dispatcher.utter_message("===== result =====")
          # dispatcher.utter_message(str(result))

          dispatcher.utter_message("bundles slot found and action bundle executed")

      else:
          dispatcher.utter_message("no bundles slot filled  inside show detailed bundle project info")

      return []



class DisplayServiceQuery(Action):


    def name(self):

      return "action_show_detailed_service_project_info"

    def run(self, dispatcher, tracker, domain):
      # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]

    # tracker.get_slot('city')[bool(tracker.get_slot('city'))] 
      dispatcher.utter_message("action give **detailed** project info being called ")

      recent_message = (tracker.latest_message)['text']

      dispatcher.utter_message(" ==== current state of tracker ======")
      # dispatcher.utter_message(tracker.current_state)

      result = None
      failure = None

      if tracker.get_slot('service'):

          # gQuery = GenerateQuery(recent_message)
          # parse_msg = gQuery.predictIntentionAndEntity()
          
          # [query, params, result] = gQuery.convertTextToQuery()
          # dispatcher.utter_message("===== Query =====")
          # dispatcher.utter_message(query)
          # dispatcher.utter_message("=== query params =====")
          # dispatcher.utter_message(str(params))
          # dispatcher.utter_message("===== result =====")
          # dispatcher.utter_message(str(result))

          dispatcher.utter_message("service slot found and action service executed")
      else:

          dispatcher.utter_message("no service slot filled inside detailed service project action")

      return []

'''
Exports lies inside bundle 
To execute query regarding exports, we need to know the value of bundles slot
'''
class DisplayExportQuery(Action):

    def name(self):

      return "action_show_exports_in_bundle"

    def run(self, dispatcher, tracker, domain):
      # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]

    # tracker.get_slot('city')[bool(tracker.get_slot('city'))] 
      dispatcher.utter_message("Export Query action ")

      recent_message = (tracker.latest_message)['text']

      # dispatcher.utter_message(tracker.current_state)

      result = None
      failure = None
      bundle_slot = tracker.get_slot('bundles')


      if tracker.get_slot('PackagesExports'):

          displayQueryOutput(recent_message, dispatcher)
          # gQuery = GenerateQuery(recent_message)
          # parse_msg = gQuery.predictIntentionAndEntity()
          
          # [query, params, result] = gQuery.convertTextToQuery(bundle_slot)
          # dispatcher.utter_message("===== Query =====")
          # dispatcher.utter_message(query)
          # dispatcher.utter_message("=== query params =====")
          # dispatcher.utter_message(str(params))
          # dispatcher.utter_message("===== result =====")
          # dispatcher.utter_message(str(result))


          dispatcher.utter_message("bundles slot found and action bundle executed")

      else:

          dispatcher.utter_message("no PackagesExports slot filled inside show exports action")

      return []

'''
Show specific node information
'''

class showNodeInformation(Action):
  
    def name(self):

          return "action_show_node_information"

    def run(self, dispatcher, tracker, domain):

      dispatcher.utter_message("show node information ")

      recent_message = (tracker.latest_message)['text']

      print(tracker.current_slot_values())

      if tracker.get_slot('node'):

          displayQueryOutput(recent_message, dispatcher)
          # gQuery = GenerateQuery(recent_message)
          # parse_msg = gQuery.predictIntentionAndEntity()
          
          # [query, params, result] = gQuery.convertTextToQuery()
          # dispatcher.utter_message("===== Query =====")
          # dispatcher.utter_message(query)
          # dispatcher.utter_message("=== query params =====")
          # dispatcher.utter_message(str(params))
          # dispatcher.utter_message("===== result =====")
          # dispatcher.utter_message(str(result))


          dispatcher.utter_message("node slot got filled and action show node information executed")

      else:

          dispatcher.utter_message("no node slot filled inside action show node information")

      return []

'''
show nodes
'''

class showAllNodes(Action):
  
    def name(self):

          return "action_show_all_nodes"

    def run(self, dispatcher, tracker, domain):

      dispatcher.utter_message("show all the nodes information ")

      recent_message = (tracker.latest_message)['text']

      dispatcher.utter_message("get current slot values ")

      print(tracker.current_slot_values())

      if tracker.get_slot('packages'):

          displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('bundles'):

          displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('services'):

          displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('compilationUnit'):

          displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('Methods'):

          displayQueryOutput(recent_message, dispatcher)

      else:

          dispatcher.utter_message("no slot filled inside action show all information")

      return []

'''
count all nodes
'''

class countAllNodes(Action):
  

    def name(self):

          return "action_count_all_nodes"


    def run(self, dispatcher, tracker, domain):

      dispatcher.utter_message("count all nodes")

      recent_message = (tracker.latest_message)['text']

      dispatcher.utter_message("get current slot values ")

      print(tracker.current_slot_values())

      if tracker.get_slot('packages'):

          displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('bundles'):

          displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('services'):

          displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('compilationUnit'):

          displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('Methods'):

          displayQueryOutput(recent_message, dispatcher)

      else:

          dispatcher.utter_message("no slot filled count all nodes")

      return []

'''
This class resets the slots
'''

class ActionRenew(Action):

    def name(self):
      return 'action_renew'


    def run(self, dispatcher, tracker, domain):

      return_slots = []

      for slot in tracker.slots:
        if slot != 'foo':
          return_slots.append(SlotSet(slot, None))

      return return_slots


def displayQueryOutput(recent_message, dispatcher, bundle_slot=None):

  gQuery = GenerateQuery(recent_message)

  parse_msg = gQuery.predictIntentionAndEntity()
  
  [query, params, result] = gQuery.convertTextToQuery(bundle_slot)
  dispatcher.utter_message("===== Query =====")
  dispatcher.utter_message(query)
  dispatcher.utter_message("=== query params =====")
  dispatcher.utter_message(str(params))
  dispatcher.utter_message("===== result =====")
  dispatcher.utter_message(str(result))

