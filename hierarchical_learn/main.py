import pickle
import numpy as np
import math

from bow import get_testset_bow_vector
from classifier_adaptor import ClassifierAdaptor
from hierarchical_learning import HierarchicalLearning



with open("../bayes/bow/01234/trainset_bow_instance_classes.pickle", 'rb') as icf:
	trainset_instance_classes = pickle.load(icf)

with open("../bayes/bow/01234/trainset_bow_classes_list.pickle", 'rb') as clf:
	trainset_classes_list = pickle.load(clf)

with open("../bayes/bow/test_zkall/testset_bow_instance_label.pickle", 'rb') as ilf:
	testset_instance_labels = pickle.load(ilf)

with open("../bayes/bow/test_zkall/testset_bow_instance_classes.pickle", 'rb') as icf:
	testset_instance_classes = pickle.load(icf)


# length of four classes
length_classes = list()
for class_list in trainset_classes_list:
	length_classes.append(len(class_list))



def get_test_instance_vector_label(test_set):
	X = list()
	Y = list()
	for iid in test_set:
		# normalize classes val
		classes_vec = list()
		for index in range(0, 4):
			dimen = [0] * length_classes[index]
			all_classes = trainset_classes_list[index]
			class_val = testset_instance_classes[iid][index]
			if class_val in all_classes:
				dimen_idx = all_classes.index(class_val)
				dimen[dimen_idx] = 1

			classes_vec += dimen

		# bow_val
		bow_vec = get_testset_bow_vector(iid)

		x = classes_vec + bow_vec
		y = int(testset_instance_labels[iid])
		X.append(x)
		Y.append(y)

	return X, Y


def validate(Y_pred, Y_true, instance_ids):
	correct_count = 0

	for idx in range(0, len(Y_true)):
		y_true = Y_true[idx]
		y_pred = Y_pred[idx]
		instance_id = instance_ids[idx]

		print( "[REPORT] instance_id: " + instance_id + " | true_label : " + str(y_true) + " | pred_label : " + str(y_pred) )
		
		if y_true == y_pred:
			correct_count += 1
		
	print("------------ Accuracy : " + str(correct_count / len(Y_true)) + "------------")




if __name__ == '__main__':
	# init classfiers
	clf_01234 = ClassifierAdaptor('HY_01234_classifier.joblib')
	clf_zk0 = ClassifierAdaptor('HY_zk0_classifier.joblib')
	clf_zk1 = ClassifierAdaptor('HY_zk1_classifier.joblib')
	clf_zk2 = ClassifierAdaptor('HY_zk2_classifier.joblib')
	clf_zk3 = ClassifierAdaptor('HY_zk3_classifier.joblib')
	clf_zk4 = ClassifierAdaptor('HY_zk4_classifier.joblib')

	# init learner
	hierarchical_clf = HierarchicalLearning()
	hierarchical_clf.set_root_classifier(clf_01234)
	second_layer_clfs = list([clf_zk0, clf_zk1, clf_zk2, clf_zk3, clf_zk4])
	hierarchical_clf.set_sub_classifiers(second_layer_clfs)
	
	test_list = list(testset_instance_labels.keys())
	X_test, Y_test = get_test_instance_vector_label(test_list)

	total_count = 0
	correct_count = 0

	for i in range(0, len(X_test)):	
		total_count += 1
		y_pred = hierarchical_clf.classify(X_test[i])

		#print("[INFO] true:" + str(y_pred) + " | pred:" + str(Y_test[i]))
		if y_pred == Y_test[i]:
			correct_count += 1

	print("Accuracy : " + str(correct_count / total_count))