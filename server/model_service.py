import pickle
import os

# load data from repo
global testset_predicts
global testset_infos
global trainset_infos

with open("repo/testset_predicts.pickle", 'rb') as tpf:
	testset_predicts = pickle.load(tpf)
with open("repo/testset_infos.pickle", 'rb') as iif:
	testset_infos = pickle.load(iif)
with open("repo/trainset_infos.pickle", 'rb') as iif:
	trainset_infos = pickle.load(iif)



def service_get_correct_count_of_labelset(label):
	correct_pred_instances = testset_predicts['correct_pred_instances']
	correct_count = 0

	for instance_id in correct_pred_instances:
		if testset_infos['instance_infos'][instance_id][6] == label:
			correct_count += 1

	return correct_count


def service_get_train_test_labels_count():
	sta_labels = list()
	sta_train_label_count = list()
	sta_test_label_count = list()

	trainset_labels_count = trainset_infos['labels_count']
	testset_labels_count = testset_infos['labels_count']
	labels = [v for v in trainset_labels_count.keys() if v in testset_labels_count.keys()]
	labels.sort()

	for label in labels:
		sta_labels.append(label)
		sta_train_label_count.append(trainset_labels_count[label])
		sta_test_label_count.append(testset_labels_count[label])

	return sta_labels, sta_train_label_count, sta_test_label_count


def service_get_testset_accuracy():
	correct_pred_num = len(testset_predicts['correct_pred_instances'])
	testset_instances_num = len(testset_predicts['testset_pred_infos'])
	return correct_pred_num / testset_instances_num


def service_get_testset_instance_info(instance_id):
	info = testset_infos['instance_infos'][instance_id]
	pred_info = testset_predicts['testset_pred_infos'][instance_id]
	return info, pred_info


def service_get_testset_infos():
	return testset_infos['instance_infos'], testset_predicts['testset_pred_infos']



