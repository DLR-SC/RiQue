from queryGeneration import GenerateQuery

class Utility:

	def getQuery(self,recent_message, dispatcher, bundle_slot=None):

		gQuery = GenerateQuery(recent_message)
		parse_msg = gQuery.predictIntentionAndEntity()
		[query, params, result] = gQuery.convertTextToQuery(bundle_slot)
		
		# restructure query
		for key, value in params.items():
			if (key in query):
				# because key present in param does nto have $ sign
				modified_key = "$" + key
				query = query.replace(modified_key, '"'+str(value)+'"')

		# dispatcher.utter_message("===== Query =====")
		dispatcher.utter_message(query)
		# dispatcher.utter_message("=== query params =====")
		# dispatcher.utter_message(str(params))
		# dispatcher.utter_message("===== result =====")
		# dispatcher.utter_message(str(result))