import os
import pickle
import numpy as np
import math

from sklearn.metrics import roc_curve, auc
#import matplotlib.pyplot as plt

global inverse_index
global label_map
global instance_tokens
global instance_classes
global classes_list 

index_file = "bow_inverse_index.pickle"
label_file = "instance_label.pickle"
instance_tokens_file = "instance_tokens.pickle"
instance_classes_file = "instance_classes.pickle"
classes_list_file = "classes_list.pickle"


def index_of_agency(agency_name, agency_lst):
	for index in range(0, len(agency_lst)):
		if agency_lst[index] == agency_name:
			break
	return index


def get_estimated_postive_poss(training_set, test_set):
	# count frequency of agency & num_instance
	# prob_agency = freq / num_instance
	num_instance = len(training_set)
	agency_freq = {}

	#print("[INFO] start calculating F(ai)...")
	for iid, c in label_map.items():
		if iid not in training_set:
			continue

		if c not in agency_freq.keys():
			agency_freq[c] = 1
		else:
			agency_freq[c] = agency_freq[c] + 1

	#print("[INFO] start calculating F(xi,ai)...")

	# count the frequency of token in the instance belonging to the agency
	# P(xi|A) = freq of token in instance belonging to the agency + 1 / num of instance belonging to the agency + 2
	token_agency_freq = []
	agency_lst = list(agency_freq.keys())
	token_lst = list(inverse_index.keys())

	# to init the 2 dimension array(frequency of token in the instance belonging to agency)
	# x-axis is tokens, y-axis is agencies
	for i in range(0, len(agency_lst)):
		token_agency_freq.append([0] * len(token_lst))

	# fill 2 dimension array
	idx_token = 0
	for token, instance_id_lst in inverse_index.items():
		print("[TRAINING] calculating the F(xi,ai) for token: " + token)

		for instance_id in instance_id_lst:
			if instance_id not in training_set:
				continue

			agency = label_map[instance_id]
			idx_agency = index_of_agency(agency, agency_lst)
			token_agency_freq[idx_agency][idx_token] = token_agency_freq[idx_agency][idx_token] + 1

		idx_token = idx_token + 1

	# count the frequency of classes value in class1, class2, class3, class4 for each agency
	classes_agency_freq = []
	for i in range(0, len(agency_lst)):
		element = []
		# for every class
		for class_idx in range(0, 4):
			temp_map = {}
			for class_val in classes_list[class_idx]:
				temp_map[class_val] = 0
			element.append(temp_map)

		classes_agency_freq.append(element)

	for instance_id, classes in instance_classes.items():
		agency = label_map[instance_id]
		idx_agency = index_of_agency(agency, agency_lst)

		for class_idx in range(0, 4):
			class_val_index = classes[class_idx]
			class_val = classes_list[class_idx][class_val_index]
			classes_agency_freq[idx_agency][class_idx][class_val] = classes_agency_freq[idx_agency][class_idx][class_val] + 1


	print("[INFO] start calculating y_socre...")
	# y_score is possibility of positive class

	y_score = []
	y_label = []

	for iid in test_set:
		positive_poss = 0

		#calculate p(1)
		positive_poss += math.log(agency_freq[1] / num_instance)

		# calculate tokens
		tokens = instance_tokens[iid]
		positive_label_index = index_of_agency(1, agency_lst)
		freq_agenc = agency_freq[1]

		for tid in range(0 , len(token_lst)):
			if token_lst[tid] in tokens:
				freq_agenc_token = token_agency_freq[positive_label_index][tid]
			else:
				freq_agenc_token = freq_agenc - token_agency_freq[positive_label_index][tid]

			positive_poss += math.log((freq_agenc_token + 1) / (freq_agenc + 2))  # smooth

		# calculate classes
		class_values = instance_classes[iid]
		for class_idx in range(0, 4):
			class_val_index = class_values[class_idx]
			class_val = classes_list[class_idx][class_val_index]
			positive_poss += math.log( (classes_agency_freq[positive_label_index][class_idx][class_val] + 1) / (freq_agenc + 2) )

		y_score.append(math.exp(positive_poss))
		y_label.append(label_map[iid])

	return y_score, y_label



if __name__ == '__main__':
	with open(index_file, 'rb') as iif:
		inverse_index = pickle.load(iif)

	with open(label_file, 'rb') as lbf:
		or_label_map = pickle.load(lbf)

	with open(instance_tokens_file, 'rb') as itf:
		instance_tokens = pickle.load(itf)

	with open(instance_classes_file, 'rb') as icf:
		instance_classes = pickle.load(icf)

	with open(classes_list_file, 'rb') as clf:
		classes_list = pickle.load(clf)


	instance_list = list(or_label_map.keys())
	all_labels = ['0', '1', '2', '3', '4']


	size = math.ceil(len(instance_list) / 5)
	chunks = []
	for c in range(0, 4):
		subset = instance_list[ c * size : c * size + size]
		chunks.append(subset)
	# last chunk
	subset = instance_list[4 * size :]
	chunks.append(subset)

	test_set = chunks[4]
	training_set = chunks[0]+ chunks[1] + chunks[2] + chunks[3]
	

	Y_score = []
	Y_real = []

	for target_label in all_labels:
		# one vs rest 	
		label_map = {}

		for instance_id, lb in or_label_map.items():
			if lb == target_label:
				label_map[instance_id] = 1
			else:
				label_map[instance_id] = 0

		# naive bayes to generate estimated possibility of positive class
		y_score, y_label = get_estimated_postive_poss(training_set, test_set)
		Y_score += y_score 
		Y_real += y_label


	# Compute micro-average ROC curve and ROC area
	fpr, tpr, _ = roc_curve(Y_real, Y_score)

	with open('fpr.pickle', 'wb') as f:
		pickle.dump(fpr, f, pickle.HIGHEST_PROTOCOL)

	with open('tpr.pickle', 'wb') as f:
		pickle.dump(tpr, f, pickle.HIGHEST_PROTOCOL)

	roc_auc = auc(fpr, tpr)
	print("---------- auc ---------")
	print(roc_auc)