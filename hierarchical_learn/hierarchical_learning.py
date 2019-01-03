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
			params_check()
			self.has_init = True

		return second_layer_classify(input, first_layer_classify(input))


	def first_layer_classify(self, input):
		first_layer_clf_result = self.root_classifier.classify(input)


	def second_layer_classify(self, input, prev_layer_clf_result):
		# get index of classfier
		index_clf = -1
		for cfg in edges_config:
			if prev_layer_clf_result == cfg[0]:
				index_clf = cfg[1]
				break

		if index_clf == -1:
			raise Exception("edges config error - can not map edge configuration")

		second_layer_classifier = self.sub_classifiers[index_clf]
		second_layer_clf_result = second_layer_classifier.classify(input)


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
				tp = tuple(i , i)
				default_edges_cfg.append(tp)

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
			if cfg not is tuple:
				raise Exception("elements of edges_config should be a tuple")






