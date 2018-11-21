import pickle
import os

# load data from repo
global testset_predicts
global testset_instance_infos

with open("repo/testset_predicts.pickle", 'rb') as tpf:
	testset_predicts = pickle.load(tpf)
with open("repo/testset_instance_infos.pickle", 'rb') as iif:
	testset_instance_infos = pickle.load(iif)


def service_get_all_labels():
	return None


def service_get_trainset_statistic():
	return None


def service_get_testset_accuracy():
	correct_pred_num = len(testset_predicts['correct_pred_instances'])
	testset_instances_num = len(testset_predicts['testset_pred_infos'])
	return correct_pred_num / testset_instances_num


def service_get_testset_labels_count():
	labels = service_get_all_labels()
	labels_count = dict()
	# init
	for lb in labels:
		labels_count[lb] = 0

	# counting
	for instance_id, info in testset_predicts['testset_pred_infos']:
		true_label = info[0]
		labels_count[true_label] += 1 

	return labels_count


def service_get_testset_instance_list():
	instance_list = list()

	for instance_id in testset_predicts.keys():
		detail = dict()
		
		info = testset_instance_infos[instance_id]
		detail['class1'] = info[0]
		detail['class2'] = info[1]
		detail['class3'] = info[2]
		detail['class4'] = info[3]
		detail['content'] = info[4]
		
		pred_info = testset_predicts[instance_id]
		detail['true_label'] = pred_info[0]
		detail['pred_label'] = pred_info[1]
		instance_list.append(detail)

	return instance_list


def service_get_testset_instance_info(instance_id):
	detail = dict()

	info = testset_instance_infos[instance_id]
	detail['class1'] = info[0]
	detail['class2'] = info[1]
	detail['class3'] = info[2]
	detail['class4'] = info[3]
	detail['content'] = info[4]
	detail['agency'] = info[5]

	pred_info = testset_predicts[instance_id]
	detail['true_label'] = pred_info[0]
	detail['pred_label'] = pred_info[1]

	return detail



