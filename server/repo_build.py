import os
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
		print('[INFO] testset_predicts pickle has been saved.')










if __name__ == '__main__':
	parse_testset_log('../bayes/log_zk04.txt')