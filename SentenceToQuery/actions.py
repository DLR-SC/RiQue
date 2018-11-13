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

      dispatcher.utter_message("action give project info being called ")

      recent_message = (tracker.latest_message)['text']

      if tracker.get_slot('project'):

          util.getQuery(recent_message, dispatcher, tracker.current_slot_values())

          # dispatcher.utter_message("project info being uttered ..")

      else:
          
          dispatcher.utter_message("no project slot is filled inside action give project information action")

      return []


class DisplayBundleDetailedQuery(Action):


    def name(self):

      return "action_show_show_detail_info_bundles"

    def run(self, dispatcher, tracker, domain):
      # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]

      dispatcher.utter_message("action show detail info bundle")

      recent_message = (tracker.latest_message)['text']

      # dispatcher.utter_message(tracker.current_state)

      if tracker.get_slot('BundlesName'):

          # dispatcher.utter_message("Slot value ")
          # dispatcher.utter_message(tracker.get_slot('BundlesName'))
          
          util.getQuery(recent_message, dispatcher)

          # dispatcher.utter_message("bundles slot found and action bundle executed")

      else:
          dispatcher.utter_message("no bundles slot filled  inside show detailed bundle project info")

      return []

'''
Get compilation units with highest number of code lines
'''

class DisplayLargestCompilationUnit(Action):


    def name(self):

      return "action_show_largest_compilationUnit"

    def run(self, dispatcher, tracker, domain):
      # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]

    # tracker.get_slot('city')[bool(tracker.get_slot('city'))] 
      dispatcher.utter_message("action show largest compilation units")

      recent_message = (tracker.latest_message)['text']

      # dispatcher.utter_message(tracker.current_state)

      if tracker.get_slot('compilationUnit'):
          # print(tracker.current_slot_values())
          util.getQuery(recent_message, dispatcher, tracker.current_slot_values())

          # dispatcher.utter_message("compilation slot found and show largest compilation unit executed")

      else:
          dispatcher.utter_message("compilationUnit is not filled")

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

      # print(tracker.current_slot_values())

      if tracker.get_slot('node'):

          util.getQuery(recent_message, dispatcher)
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

      # print(tracker.current_slot_values())

      if tracker.get_slot('packages'):

          util.getQuery(recent_message, dispatcher)

      elif tracker.get_slot('bundles'):

          util.getQuery(recent_message, dispatcher)

      elif tracker.get_slot('services'):

          util.getQuery(recent_message, dispatcher)

      elif tracker.get_slot('compilationUnit'):

          util.getQuery(recent_message, dispatcher)

      elif tracker.get_slot('Methods'):

          util.getQuery(recent_message, dispatcher)

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

      # print(tracker.current_slot_values())

      if tracker.get_slot('packages'):

          util.getQuery(recent_message, dispatcher)

      elif tracker.get_slot('bundles'):

          util.getQuery(recent_message, dispatcher)

      elif tracker.get_slot('services'):

          util.getQuery(recent_message, dispatcher)

      elif tracker.get_slot('compilationUnit'):

          util.getQuery(recent_message, dispatcher)

      elif tracker.get_slot('Methods'):

          util.getQuery(recent_message, dispatcher)

      else:

          dispatcher.utter_message("no slot filled count all nodes")

      return []

'''
This class resets the slots
reset all the slots except project 
because this slot is not being used for other intents
'''

class ActionReset(Action):

    def name(self):
      return 'action_reset'


    def run(self, dispatcher, tracker, domain):

      return_slots = []

      for slot in tracker.slots:
        if slot != 'project':
          return_slots.append(SlotSet(slot, None))

      return return_slots
