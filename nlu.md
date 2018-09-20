## intent:greeting
- hello
- hi
- howdee
- hi there
- good morning

## intent:find_entity_by_name_or_id
- find [region](entity_type) [DOE](unit_name)
- find [package](entity_type:region) [DOE](unit_name)
- where is [DOE](unit_name)
- focus on [DOE](unit_name)
- show me [building](entity_type) [DOE](unit_name)
- show me [class](entity_type:building) [DOE](unit_name)
- show me [compilation unit](entity_type:building) [DOE](unit_name)
- i want to have a look at this [region](entity_type)
- find the [island](entity_type) named [DOE](unit_name)
- find the [bundle](entity_type:island) named [DOE](unit_name)
- show me [Evaluation](unit_name)
- show me [Writer](unit_name)
- show me [Execution](unit_name)
- show me [Excel](unit_name)
- show me [Input Provider](unit_name)
- show me [Joiner Component](unit_name)
- show me [DOE](unit_name)

## intent:show_entity
- show all [services](entity_to_display) 
- show all [service](entity_to_display:services)
- show all [exports](entity_to_display) 
- show all [imports](entity_to_display) 
- show all [dependencies](entity_to_display:exports) 
- show all [export](entity_to_display:exports)
- show [services](entity_to_display)
- visualize the [services](entity_to_display)
- visualize [services](entity_to_display)
- i want to see the [services](entity_to_display)
- display the [services](entity_to_display)

## intent:hide_entity
- i dont need the [service](entity_to_display:services) any longer
- close [services](entity_to_display)
- hide [services](entity_to_display)
- hide [services](entity_to_display)

## intent:graph_db_query_most
- which bundle contains the highest number of [exports](graph_db_query)
- find the bundle with the highest number of [exports](graph_db_query)
- which bundle has the highest number of [exports](graph_db_query)
- which bundle contains the highest number of [imports](graph_db_query)
- find the bundle with the highest number of [imports](graph_db_query)
- which bundle has the highest number of [imports](graph_db_query)
- which bundle contains the highest number of [services](graph_db_query)
- which bundle contains the highest number of [classes](graph_db_query)
- which bundle contains the highest number of [packages](graph_db_query)
