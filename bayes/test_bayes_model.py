import os
import csv
import math
import pickle

index_file = "bow_inverse_index.pickle"
label_file = "test_set_instance_label.pickle"
instance_tokens_file = "test_set_instance_tokens.pickle"
instance_classes_file = "test_set_instance_classes.pickle"
classes_list_file = "classes_list.pickle"

global inverse_index
global label_map
global instance_tokens
global instance_classes
global classes_list
global agency_freq
global token_agency_freq
global classes_agency_freq


def index_of_agency(agency_name, agency_lst):
	for index in range(0, len(agency_lst)):
		if agency_lst[index] == agency_name:
			break
	return index

#===================== main ====================
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

with open("agency_freq.pickle", 'rb') as clf:
	agency_freq = pickle.load(clf)

with open("token_agency_freq.pickle", 'rb') as clf:
	token_agency_freq = pickle.load(clf)

with open("classes_agency_freq.pickle", 'rb') as clf:
	classes_agency_freq = pickle.load(clf)	


correct_instance_ids = []
error_instance_ids = []

test_set = instance_tokens.keys()
agency_lst = [0, 1, 2, 3, 4]
num_instance = 40000
token_lst = list(inverse_index.keys())



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