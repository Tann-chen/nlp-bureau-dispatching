# The script is to edit the lable(last column) in existing csv data and count the instances of each label in new csv data
# Files Included : 
#		* label.config  -  label rules
#		* input.csv
#		* output.csv  
# Author : Tann Chen

import os
import csv
import pickle 


config_agency_label = {}
label_instance_counter = {}

# read label.conf file 
with open("label.conf", 'r') as f:
	config_content = f.read()
	config_list = config_content.split('\n')
	for conf in config_list:
		conf_agency = conf.split(',')[0]
		label = conf.split(',')[1]
		config_agency_label[conf_agency] = label
		label_instance_counter[label] = 0

# edit label in csv
input_file_path = "../data/4k_testset.csv"
output_file_path = "4k_testset_zk04.csv"

source_file = open(input_file_path, 'r', encoding='gb18030')
target_file = open(output_file_path, 'w', encoding='gb18030', newline='')
reader = csv.reader(source_file)
writer = csv.writer(target_file)

count = 0
try:
	for row in reader:
		if row[0] != 'ID':
			count += 1
			agency_name = row[-2]
			if agency_name in config_agency_label.keys():
				new_label = config_agency_label[agency_name]
				row[-1] = new_label
				label_instance_counter[new_label] += 1
			else:
				print("[ERROR] the agency name is out of the label.conf :" + agency_name)
				continue  

		writer.writerow(row)

except csv.Error as e:
	source_file.close()
	target_file.close()
	print("[ERROR]")


print("---------- Count of each label -----------")
print("Total instances : " + str(count))
for a, c in label_instance_counter.items():
	print("[REPORT]" + a + " : " + str(c))
