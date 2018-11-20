import pickle
import numpy


with open('bayes/bow/trainset_bow_instance_label.pickle', 'rb') as tdf:
	train_dataset = pickle.load(tdf)

label_count = dict()

for instance_id, label in train_dataset.items():
	label = int(label)
	if label not in label_count.keys():
		label_count[label] = 1
	else:
		label_count[label] += 1


print('------------ END ------------')
label_count_keys = list(label_count.keys())
label_count_keys.sort()


for label in label_count_keys:
	print(str(label) + ' : ' + str(label_count[label])) 

