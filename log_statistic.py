import matplotlib.pyplot as plt
import csv



# log format : [REPORT] true_label : 0 | pred_label : 1

base_labels = []

def count_error_labeling(error_label, error_label_dict):
	if error_label in error_label_dict.keys():
		error_label_dict[error_label] += 1
	else:
		error_label_dict[error_label] = 1


all_labels = set()
correct_labeling = dict()

# error_labeling dict of dict : {true_label:{error_label_1: 1, error_label_2 :1, ....}......}
error_labeling = dict()

with open("test_qzk.txt", 'r') as file:
	log_content = file.read()
	log_rows = log_content.split('\n')

for row in log_rows:
	if not row.startswith('[REPORT]'):
		continue
	# parse
	row_elements = row[8:].replace(' ', '').split('|')
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
all_labels = list(all_labels)
all_labels.sort()

# count the distribution of true label
label_correct_counts = dict()
label_error_counts = dict()

for label in all_labels:
	correct_count = 0
	if label in correct_labeling.keys(): 
		correct_count = correct_labeling[label]

	error_count = 0
	if label in error_labeling.keys():
		for k, c in error_labeling[label].items():
			error_count += c

	label_correct_counts[label] = correct_count
	label_error_counts[label] = error_count

# plot the distribution of true labels
x = list()
y_correct = list()
y_error = list()

for l in all_labels:
	if l not in base_labels:
		x.append(l)
		y_correct.append(label_correct_counts[l])
		y_error.append(label_error_counts[l])



plt.bar(x, y_correct, color='green')
plt.bar(x, y_error, color='red', bottom=y_correct)
plt.show()



# count the error matrix
# X-axis: true label; Y-axis: pred label

target_file = open("details.csv", 'w', encoding='gb18030', newline='')
writer = csv.writer(target_file)

try:
	title = ['']
	for label in all_labels:
		title.append(label)
	writer.writerow(title)

	for true_label in all_labels:
		content = list()
		content.append(true_label)

		for pred_label in all_labels:
			if true_label == pred_label:
				content.append(label_correct_counts[true_label])
			else:
				num = 0
				if true_label in error_labeling.keys():
					if pred_label in error_labeling[true_label].keys():
						num = error_labeling[true_label][pred_label]
				content.append(num)

		writer.writerow(content)
except csv.Error as e:
	target_file.close()
	







