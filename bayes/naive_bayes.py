import os
import csv
import math
import pickle

# inversed_index and instance_label (baf_of_word.py) are the foundation of the implementaion.

index_file = "bow_inverse_index.pickle"
label_file = "instance_label.pickle"
instance_tokens_file = "instance_tokens.pickle"
instance_classes_file = "instance_classes.pickle"
classes_list_file = "classes_list.pickle"

global inverse_index
global label_map
global instance_tokens
global instance_classes
global classes_list


def index_of_agency(agency_name, agency_lst):
	for index in range(0, len(agency_lst)):
		if agency_lst[index] == agency_name:
			break
	return index


# training_set, test_set : instance ids
def naive_bayes(training_set, test_set):
	# count frequency of agency & num_instance
	# prob_agency = freq / num_instance
	num_instance = len(training_set)
	agency_freq = {}

	print("[INFO] start calculating F(ai)...")
	for iid, c in label_map.items():
		if iid not in training_set:
			continue

		if c not in agency_freq.keys():
			agency_freq[c] = 1
		else:
			agency_freq[c] = agency_freq[c] + 1

	print("[INFO] start calculating F(xi,ai)...")
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

	print("[INFO] finish training...")


	# testing
	print("[INFO] start testing...")
	correct_instance_ids = []
	error_instance_ids = []

	for iid in test_set:
		tokens = instance_tokens[iid]
		
		# calculate possibility for every agency
		# only can learn from the agencies appeared in test set		
		agency_possible = [1] * len(agency_lst)

		# calculate p(ai)
		agency_idx = 0
		for freq in agency_freq.values():
			agency_possible[agency_idx] = agency_possible[agency_idx] + math.log10(freq / num_instance)
			agency_idx = agency_idx + 1


		# calculate tokens
		for aid in range(0, len(agency_lst)):
			freq_agenc = agency_freq[agency_lst[aid]]

			for tid in range(0, len(token_lst)):
				if token_lst[tid] in tokens:
					freq_agenc_token = token_agency_freq[aid][tid]
				else:
					freq_agenc_token = freq_agenc - token_agency_freq[aid][tid]

				agency_possible[aid] = agency_possible[aid] + math.log10( (freq_agenc_token + 1) / (freq_agenc + 2) ) # smooth


		# calculate classes
		class_values = instance_classes[iid]
		for class_idx in range(0, 4):
			class_val_index = class_values[class_idx]
			class_val = classes_list[class_idx][class_val_index]

			for aid in range(0, len(agency_lst)):
				freq_agenc = agency_freq[agency_lst[aid]]
				agency_possible[aid] = agency_possible[aid] + math.log10( (classes_agency_freq[aid][class_idx][class_val] + 1) / (freq_agenc + 2) )


		# get the agency class with max possible
		max_id = 0 
		max_val = agency_possible[0]

		for i in range(1, len(agency_possible)):
			if agency_possible[i] > max_val:
				max_val = agency_possible[i]
				max_id = i

		estimate_label = agency_lst[max_id]
		#print("[INFO] estimate : " + str(iid) + " is " +  estimate_label)

		if estimate_label == label_map[iid]:
			correct_instance_ids.append(iid)
			#print("[INFO] correct estimate :" + str(iid))
		else:
			error_instance_ids.append(iid)
			#print("[INFO] error estimate :" + str(iid))

	print("================== test finish =================")
	print("Accuracy : " + str(len(correct_instance_ids) / len(test_set)))


if __name__ == '__main__':
	with open(index_file, 'rb') as iif:
		inverse_index = pickle.load(iif)

	with open(label_file, 'rb') as lbf:
		label_map = pickle.load(lbf)

	with open(instance_tokens_file, 'rb') as itf:
		instance_tokens = pickle.load(itf)

	with open(instance_classes_file, 'rb') as icf:
		instance_classes = pickle.load(icf)

	with open(classes_list_file, 'rb') as clf:
		classes_list = pickle.load(clf)



	instance_list = list(label_map.keys())
	size = math.ceil(len(instance_list) / 5)
	chunks = []

	for c in range(0, 4):
		subset = instance_list[ c * size : c * size + size]
		chunks.append(subset)
	# last chunk
	subset = instance_list[4 * size :]
	chunks.append(subset)

	# cross validation
	for i in range(0, 5):
		# build test set & training set
		test_set = chunks[i]
		training_set = []
		for j in range(0, 5):
			if j != i:
				training_set = training_set + chunks[j]

		# training
		print("[INFO] training set size :" + str(len(training_set)))
		print("[INFO] test set size :" + str(len(test_set)))
		print("[INFO] start training...")
		naive_bayes(training_set, test_set)






