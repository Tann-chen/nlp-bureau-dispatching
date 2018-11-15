# log format : [REPORT] true_label : 0 | pred_label : 1


all_labels = set()
correct_labeling = dict()

# error_labeling dict of dict : {true_label:{error_label_1: 1, error_label_2 :1, ....}......}
error_labeling = dict()


def count_error_labeling(error_label, error_label_dict):
	if error_label in error_label_dict.keys():
		error_label_dict[error_label] += 1
	else:
		error_label_dict[error_label] = 1


with open("log_file.txt", 'r') as file:
	log_content = file.read()
	log_rows = log_content.split('\n')

for row in log_rows:
	if not row.startswith('[REPORT]'):
		continue
	# parse
	row_elements = row[8:].replace(' ', '')split('|')
	true_label = int(row_elements[0].split(':')[1].strip())
	pred_label = int(row_elements[1].split(':')[1].strip())

	all_labels.add(true_label)
	all_labels.add(pred_label)

	# statistic
	if true_label == pred_label:
		if true_label not in correct_labeling.keys():
			correct_labeling[true_label] = 1
		else:
			correct_labeling[true_label] += 1
	
	elif true_label in error_labeling.keys():
		error_label_dict = error_labeling[true_label]
		count_error_labeling(pred_label, error_label_dict)
	else:
		error_label_dict = dict()
		count_error_labeling(pred_label, error_label_dict)
		error_labeling[true_label] = error_label_dict


# process the count
all_labels = list(all_labels).sort()

# count the distribution of true label
label_counts = [0] * len(all_labels)
for idex in all_labels:
	correct_count = correct_labeling[idex]
	error_count = 0
	for k, c in error_labeling[idex].items():
		error_count += c
	label_counts[idex] = correct_count + error_count
# plot the distribution of true labels


# count the error matrix
# X-axis: true label; Y-axis: pred label
error_matrix = []
for i in range(len(all_labels)):
	error_matrix.append([0] * len(all_labels))

for true_label in range(len(all_labels)):
	for pred_label in range(len(all_labels)):

		if true_label == pred_label:
			error_matrix[true_label][pred_label] = correct_labeling[true_label]
		else:
			num = 0
			if true_label in error_labeling.keys():
				if pred_label in error_labeling[true_label].keys():
					num = error_labeling[true_label][pred_label]
			error_matrix[true_label][pred_label] = num
# plot error matrix 














