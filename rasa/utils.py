from queryGeneration import GenerateQuery

class Utility:

	def displayQueryOutput(self,recent_message, dispatcher, bundle_slot=None):

		gQuery = GenerateQuery(recent_message)
		parse_msg = gQuery.predictIntentionAndEntity()
		[query, params, result] = gQuery.convertTextToQuery(bundle_slot)
		dispatcher.utter_message("===== Query =====")
		dispatcher.utter_message(query)
		dispatcher.utter_message("=== query params =====")
		dispatcher.utter_message(str(params))
		dispatcher.utter_message("===== result =====")
		dispatcher.utter_message(str(result))