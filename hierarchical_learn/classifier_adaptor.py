from sklearn.externals import joblib


class ClassifierAdaptor:
	def __init__(self, model_file):
		self.classifier = None
		set_classifier(model_file)


	def set_classifier(self, model_file):
		self.classifier = joblib.load(model_file)

	"""
	@param input is vector after preprocessing
	"""
	def classify(self, input):
		pred_label = self.classifier.predict(input)[0]


