import os
import csv
import pickle

def parse_testset_log(file_path):
	testset_predicts = dict()

	with open(file_path, 'r') as file:
		log_content = file.read()
		log_rows = log_content.split('\n')

		testset_pred_infos = dict()
		correct_pred_instances = list()
		error_pred_instances = list()

		for row in log_rows:
			if not row.startswith('[REPORT]'):
				continue
			
			# parse row
			elements = row[8 :].replace(' ', '').split('|')
			instance_id = int( elements[0].split(':')[1].strip() )
			true_label = int( elements[1].split(':')[1].strip() )
			pred_label = int( elements[2].split(':')[1].strip() )
			
			# add info to testset_pred_infos
			info_tuple = tuple( (true_label, pred_label) )
			testset_pred_infos[instance_id] = info_tuple

			# records correct and error
			if pred_label == true_label:
				correct_pred_instances.append(instance_id)
			else:
				error_pred_instances.append(instance_id)

	# dump to pickle
	testset_predicts['testset_pred_infos'] = testset_pred_infos
	testset_predicts['correct_pred_instances'] = correct_pred_instances
	testset_predicts['error_pred_instances'] = error_pred_instances

	with open('repo/testset_predicts.pickle', 'wb') as f:
		pickle.dump(testset_predicts, f, pickle.HIGHEST_PROTOCOL)
		print('[INFO] testset predicts infos pickle has been saved.')


def parse_testset_csv(file_path):
	sf = open(file_path, 'r', encoding='gb18030')
	reader = csv.reader(sf)

	instance_infos = dict()
	testset_labels_count = dict()

	for row in reader:
		if row[0] == 'ID':
			continue
		
		instance_id = int(row[0])
		class_1 = row[2]
		class_2 = row[3]
		class_3 = row[4]
		class_4 = row[5]
		content = row[6]
		agency = row[8]
		label = int(row[9])

		# add instance infos
		instance_infos[instance_id] = tuple( (class_1, class_2, class_3, class_4, content, agency, label) )

		# add test labels count
		if label not in testset_labels_count.keys():
			testset_labels_count[label] = 1
		else:
			testset_labels_count[label] += 1

	# dump
	dump = dict()
	dump['instance_infos'] = instance_infos
	dump['labels_count'] = testset_labels_count
	with open('repo/testset_infos.pickle', 'wb') as f:
		pickle.dump(dump, f, pickle.HIGHEST_PROTOCOL)
		print('[INFO] testset infos pickle has been saved.')


# ignore
def parse_label_agency_map(file_path):
	label_agency_map = dict()

	with open(file_path, 'r') as file:
		label_entries = file.read().split('\n')
		
	for entry in label_entries:
		agency_name = entry.split(',')[0]
		label = int(entry.split(',')[1])
		label_agency_map[label] = agency_name

	with open('repo/testset_label_agency_map.pickle', 'wb') as f:
		pickle.dump(label_agency_map, f, pickle.HIGHEST_PROTOCOL)
		print('[INFO] testset_label_agency_map pickle has been saved.')


def parse_trainset_csv(file_path):
	sf = open(file_path, 'r', encoding='gb18030')
	reader = csv.reader(sf)
	trainset_labels_count = dict()
	trainset_agencies_count = dict()

	for row in reader:
		if row[0] == 'ID':
			continue

		agency = row[8]
		label = int(row[9])

		# add labels count
		if label not in trainset_labels_count.keys():
			trainset_labels_count[label] = 1
		else:
			trainset_labels_count[label] += 1
		# add agency count
		if agency not in trainset_agencies_count.keys():
			trainset_agencies_count[agency] = 1
		else:
			trainset_agencies_count[agency] += 1

	#dump
	dump = dict()
	dump['labels_count'] = trainset_labels_count
	dump['agencies_count'] = trainset_agencies_count
	with open('repo/trainset_infos.pickle', 'wb') as f:
		pickle.dump(dump, f, pickle.HIGHEST_PROTOCOL)
		print('[INFO] trainset infos pickle has been saved.')









if __name__ == '__main__':
	parse_testset_log('../bayes/log_zk04.txt')
	parse_testset_csv('../data/4k_testset_zk04.csv')
	parse_trainset_csv('../data/4w_trainset_zk04.csv')