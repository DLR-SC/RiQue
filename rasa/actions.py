from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
import pypher
from pypher import Pypher, __
from pypher.builder import Param
from utils import Utility
from rasa_core.events import AllSlotsReset, Restarted

util = Utility()

class DisplayGeneralQuery(Action):


    def name(self):

      return "action_give_project_information"

    def run(self, dispatcher, tracker, domain):
      # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]

    # tracker.get_slot('city')[bool(tracker.get_slot('city'))] 
      dispatcher.utter_message("action give project info being called ")

      recent_message = (tracker.latest_message)['text']

      dispatcher.utter_message(" ==== current state of tracker ======")

      dispatcher.utter_message("project slot value")
      dispatcher.utter_message(tracker.get_slot('project'))

      if tracker.get_slot('project'):

          util.displayQueryOutput(recent_message, dispatcher)

          dispatcher.utter_message("project info being uttered ..")

      else:
          
          dispatcher.utter_message("no project slot is filled inside action give project information action")

      return []


class DisplayBundleDetailedQuery(Action):


    def name(self):

      return "action_show_show_detail_info_bundles"

    def run(self, dispatcher, tracker, domain):
      # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]

    # tracker.get_slot('city')[bool(tracker.get_slot('city'))] 
      dispatcher.utter_message("action show detail info bundle")

      recent_message = (tracker.latest_message)['text']

      # dispatcher.utter_message(tracker.current_state)

      if tracker.get_slot('BundlesName'):

          dispatcher.utter_message("Slot value ")
          dispatcher.utter_message(tracker.get_slot('BundlesName'))
          
          util.displayQueryOutput(recent_message, dispatcher)

          dispatcher.utter_message("bundles slot found and action bundle executed")

      else:
          dispatcher.utter_message("no bundles slot filled  inside show detailed bundle project info")

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

          util.displayQueryOutput(recent_message, dispatcher)
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

          util.displayQueryOutput(recent_message, dispatcher)
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

          util.displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('bundles'):

          util.displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('services'):

          util.displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('compilationUnit'):

          util.displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('Methods'):

          util.displayQueryOutput(recent_message, dispatcher)

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

          util.displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('bundles'):

          util.displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('services'):

          util.displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('compilationUnit'):

          util.displayQueryOutput(recent_message, dispatcher)

      elif tracker.get_slot('Methods'):

          util.displayQueryOutput(recent_message, dispatcher)

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


# def displayQueryOutput(recent_message, dispatcher, bundle_slot=None):

#   gQuery = GenerateQuery(recent_message)

#   parse_msg = gQuery.predictIntentionAndEntity()
  
#   [query, params, result] = gQuery.convertTextToQuery(bundle_slot)
#   dispatcher.utter_message("===== Query =====")
#   dispatcher.utter_message(query)
#   dispatcher.utter_message("=== query params =====")
#   dispatcher.utter_message(str(params))
#   dispatcher.utter_message("===== result =====")
#   dispatcher.utter_message(str(result))