## greet
* greet
  - utter_greet

## mood happy
* mood_great
  - utter_happy

## looking for restaurants
* findRestaurantsByCity
  - action_check_restaurants
* showDetailedRestaurantInfo
  - action_show_detailed_restaurant_info

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_no_worries
  - utter_cheer_up
  - utter_did_that_help
* mood_affirm
  - utter_happy

## sad path 3
* mood_unhappy
  - utter_no_worries

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* mood_deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## name introduction
* my_name_is
  - utter_my_name_is
  - utter_how_can_i_help_you

## info about restaurant example
* findRestaurantsByCity
  - action_check_restaurants
* showDetailedRestaurantInfo
  - action_show_detailed_restaurant_info

## project description
* showProjectInformation
  - action_give_project_information

## bundles information
* showDetailedBundleProjectInfo
  - action_show_detailed_bundle_project_info
* showExportsInBundle
  - action_show_exports_in_bundle

## detailed service description
* showDetailedServiceProjectInfo
  - action_show_detailed_service_project_info

## search for specific node information
* showNodeInformation
  - action_show_node_information

