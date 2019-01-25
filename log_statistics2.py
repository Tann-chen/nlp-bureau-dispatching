import matplotlib.pyplot as plt
import csv

labels = list()
counts = list()


with open("log_count.txt", 'r') as file:
	log_content = file.read()
	log_rows = log_content.split('\n')

for row in log_rows:
	if not row.startswith('[REPORT]'):
		continue
	# parse
	row_elements = row[8:].replace(' ', '').split(':')
	label = int(row_elements[0].strip())
	count = int(row_elements[1].strip())
	print(str(label) + " " + str(count))

	labels.append(label)
	counts.append(count)

plt.bar(labels, counts, color='blue')
plt.xlabel("classes")
plt.ylabel("number of instances")
plt.title("Distribution of training data for each class")
plt.show()