from classifier_adaptor import ClassifierAdaptor 


class HierarchicalLearning:
	def __init__(self):
		self.root_classifier = None
		self.sub_classifiers = None
		self.edges_config = None
		self.has_init = False


	def classify(self, input):
		# init
		if self.has_init == False:
			self.params_check()
			self.has_init = True

		return self.second_layer_classify(input, self.first_layer_classify(input))


	def first_layer_classify(self, input):
		return self.root_classifier.get_predict_proba(input)


	def second_layer_classify(self, input, prev_layer_clf_result):
		# get index of classfier
		# index_clf = -1
		# for cfg in self.edges_config:
		# 	if prev_layer_clf_result == cfg[0]:
		# 		index_clf = cfg[1]
		# 		break	

		# if index_clf == -1:
		# 	raise Exception("edges config error - can not map edge configuration")

		# second_layer_classifier = self.sub_classifiers[index_clf]
		# second_layer_clf_result = second_layer_classifier.classify(input)
		# return second_layer_clf_result

		# experiment 1
		prob_max = -1
		final_class = -1
		
		for i in range(0, len(self.sub_classifiers)):
			prev_prob = prev_layer_clf_result[i]
			clf_prob = self.sub_classifiers[i].get_predict_proba(input)
			clf_classes = self.sub_classifiers[i].get_classes()

			for ii in range(0, len(clf_classes)):
				if clf_classes[ii] not in (0, 1, 2, 3, 4) and (clf_prob[ii]) > prob_max:
					prob_max = clf_prob[ii]
					final_class = clf_classes[ii]

		return final_class

		
	def params_check(self):
		if self.root_classifier == None:
			raise Exception("Never set root_classifier")
		if self.sub_classifiers == None:
			raise Exception("Never set sub_classifiers")
		if self.edges_config == None:
			# set default values
			num_sub_clf = len(self.sub_classifiers)
			default_edges_cfg = list()
			for i in range(num_sub_clf):
				tp = tuple((i , i))
				default_edges_cfg.append(tp)
			self.edges_config = default_edges_cfg

		if len(self.sub_classifiers) != len(self.edges_config):
			raise Exception("edges_config & sub_classifiers are not mapping")



	def set_root_classifier(self, root_classifier):
		if not isinstance(root_classifier, ClassifierAdaptor):
			raise Exception("root_classifier should be a ClassifierAdaptor")
		self.root_classifier = root_classifier


	def set_sub_classifiers(self, sub_classifiers):
		if type(sub_classifiers) is not list:
			raise Exception("sub_classifiers should be a list")

		for sub_clf in sub_classifiers:
			if not isinstance(sub_clf, ClassifierAdaptor):
				raise Exception("elements of sub_classifiers should be a ClassifierAdaptor")
		self.sub_classifiers = sub_classifiers


	def set_edges_config(self, edges_config):
		if type(edges_config) is not list:
			raise Exception("edges_config should be a list")
		for cfg in edges_config:
			if cfg is not tuple:
				raise Exception("elements of edges_config should be a tuple")






