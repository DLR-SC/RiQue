from queryGeneration import GenerateQuery

class Utility:

	def getQuery(self,recent_message, dispatcher, bundle_slot=None):

		gQuery = GenerateQuery(recent_message)
		parse_msg = gQuery.predictIntentionAndEntity()
		[query, params, result, extracted_intent] = gQuery.convertTextToQuery(bundle_slot)
		
		# restructure query
		for key, value in params.items():
			if (key in query):
				# because key present in param does nto have $ sign
				modified_key = "$" + key
				query = query.replace(modified_key, '"'+str(value)+'"')

		# dispatcher.utter_message("===== Query =====")
		dispatcher.utter_message(query)
		intents = self.standarizeIntentNames()
		dispatcher.utter_message(intents[str(extracted_intent)])
		# dispatcher.utter_message("=== query params =====")
		# dispatcher.utter_message(str(params))
		# dispatcher.utter_message("===== result =====")
		# dispatcher.utter_message(str(result))

	def standarizeIntentNames(self):

		intents = {}
		intents['greet'] = 'Greet'
		intents['goodbye'] = 'Good Bye'
		intents['showProjectInformation'] = 'Show project information'
		intents['showNodeInformation'] = 'Show node information'
		intents['showAllNodes'] = 'Show all nodes'
		intents['my_name_is'] = 'Greet with name'
		intents['countAllNodes'] = 'Count all nodes'
		intents['showDetailInfoBundles'] = 'Show information about specific bundle'
		intents['showLargestCompilationUnit'] = 'Show largest compilation unit'

		return intents


