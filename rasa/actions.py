from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
import pypher
from pypher import Pypher, __
from pypher.builder import Param
from queryGeneration import GenerateQuery

# import logging 

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

          result = "It got executed"
          dispatcher.utter_message("action_check_restaurants being called ..")
          return []


      else:
          failure = "slot does not detected"
          dispatcher.utter_message("no city slot being called")
          return []




        # cuisine = tracker.get_slot('cuisine')
        # q = "select * from restaurants where cuisine='{0}' limit 1".format(cuisine)
        # result = db.query(q)

        # return [SlotSet("matches", result if result is not None else [])]
      

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

          gQuery = GenerateQuery(recent_message)
          parse_msg = gQuery.predictIntentionAndEntity()
          
          [query, params, result] = gQuery.convertTextToQuery()
          dispatcher.utter_message("===== Query =====")
          dispatcher.utter_message(query)
          dispatcher.utter_message("=== query params =====")
          dispatcher.utter_message(str(params))
          dispatcher.utter_message("===== result =====")
          dispatcher.utter_message(str(result))

          # print ("parse msg")

          # result = "project info show bitte"
          dispatcher.utter_message("project info being uttered ..")

      else:
          failure = "project slot does not detected"
          dispatcher.utter_message("no project info action being called")


      return []
      # return [SlotSet("project", result if result is not None else failure)]

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

          gQuery = GenerateQuery(recent_message)
          parse_msg = gQuery.predictIntentionAndEntity()
          
          [query, params, result] = gQuery.convertTextToQuery()
          dispatcher.utter_message("===== Query =====")
          dispatcher.utter_message(query)
          dispatcher.utter_message("=== query params =====")
          dispatcher.utter_message(str(params))
          dispatcher.utter_message("===== result =====")
          dispatcher.utter_message(str(result))


          dispatcher.utter_message("bundles slot found and action bundle executed")

      else:
          failure = "project slot does not detected"
          dispatcher.utter_message("no project info action being called")

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
          failure = "project slot does not detected"
          dispatcher.utter_message("no project info action being called")

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

      dispatcher.utter_message("current slot values ")
      dispatcher.utter_message(tracker.current_slot_values())
      if tracker.get_slot('PackagesExports'):

          gQuery = GenerateQuery(recent_message)
          parse_msg = gQuery.predictIntentionAndEntity()
          
          [query, params, result] = gQuery.convertTextToQuery(bundle_slot)
          # dispatcher.utter_message("===== Query =====")
          # dispatcher.utter_message(query)
          # dispatcher.utter_message("=== query params =====")
          # dispatcher.utter_message(str(params))
          # dispatcher.utter_message("===== result =====")
          # dispatcher.utter_message(str(result))


          dispatcher.utter_message("bundles slot found and action bundle executed")

      else:
          failure = "project slot does not detected"
          dispatcher.utter_message("no project info action being called")

      return []