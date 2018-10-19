import os
import csv
import json
import re
import traceback
import pickle
import requests
from bs4 import BeautifulSoup



def load_resource():
	file_path = "valid5000.csv"
	source_file = open(file_path, 'r', encoding='gb18030')
	reader = csv.reader(source_file)

	regexp_number = re.compile('^[0-9a-zA-Z]*$')
	regexp_punct = re.compile("^[\s+\!\/_,$%^*(+\"\')]+|[:：+——()?【】“”！，。？、~@#￥%……&*（）. 〉《 》〔〕；～ ％]$")

	stop_words_lst = ["市民", "来电", "咨询", "反映", "职能", "规定", "局"]
	NI_suffix_tuple = ("局", "队", "所", "会", "中心", "部门")
	inverse_index = {}
	label_map = {}
	instance_id = -1

	for row in reader:
		payload = {}
		instance_id = instance_id + 1
		label = row[12] # agency label
		payload['s'] = row[7]	#query content
		payload['f'] = 'xml'
		payload['t'] = 'ner'
		response = requests.post("http://127.0.0.1:12345/ltp", data=payload, timeout=5)
		soup = BeautifulSoup(response.text, 'html.parser')
		word_tags = soup.findAll('word')

		buffers = []

		for w in word_tags:
			token = w['cont']
			pos = w['pos']
			ner = w['ne']

			# rm stop words
			if token in stop_words_lst and ner is 'O':
				continue

			# merge continuous nouns
			if ner.startswith('B-') or ner.startswith('I-'):
				buffers.append(token)
				continue

			if ner.startswith('E-'):
				buffers.append(token)
				token = ''.join(buffers)
				buffers.clear()

			# note the NER
			if ner is not 'O':
				pos = ner[-2:]

			# filter numbers & punct
			if regexp_number.match(token.strip()):
				print("[INFO] invalid token : alphnum")
				continue
			if regexp_punct.match(token.strip()) or pos == 'wp':
				print("[INFO] invalid token : punctuation")
				continue

			# custom rules
			if (pos == 'j' or pos == 'n') and len(token) >=3 and token.endswith(NI_suffix_tuple):
				pos = 'Ni'
				print("[INFO] pos of token should be Ni : " + token)

			# build inverse index
			if pos not in ('Ni', 'Ns', 'n', 'j'):
				print("exclusive :" + token + ":" + pos)   # print, but throw out
			elif token in inverse_index.keys():
				instances_set = inverse_index[token]
				instances_set.add(instance_id)
				print("add :" + token)
			else:
				new_set = set()
				new_set.add(instance_id)
				inverse_index[token] = new_set
				print("add :" + token)

		print("-----------------------------")
		label_map[instance_id] = label

	print("================ end =============")
	print(len(list(inverse_index.keys())))


	with open('bow_inverse_index.pickle', 'wb') as f:
		pickle.dump(inverse_index, f, pickle.HIGHEST_PROTOCOL)

	with open('instance_label.pickle', 'wb') as f:
		pickle.dump(label_map, f, pickle.HIGHEST_PROTOCOL)



def build_bag_of_word():
	index_file = "bow_inverse_index.pickle"
	label_file = "instance_label.pickle"

	with open(index_file, 'rb') as iif:
		inverse_index = pickle.load(iif)

	with open(label_file, 'rb') as lbf:
		label_map = pickle.load(lbf)


	instance_ids = list(label_map.keys())
	tokens = list(inverse_index.keys())

	# build matrix
	matrix = []

	for iid in instance_ids:
		vector = [0]* len(tokens)
		for kid in range(0, len(tokens)):
			if iid in inverse_index[tokens[kid]]:
				vector[kid] = 1

		matrix.append(vector)

	# build labels
	labels = ['']* len(instance_ids)

	for iid in instance_ids:
		labels[iid] = label_map[iid]

	with open('matrix.pickle', 'wb') as f:
		pickle.dump(matrix, f, pickle.HIGHEST_PROTOCOL)

	with open('labels.pickle', 'wb') as f:
		pickle.dump(labels, f, pickle.HIGHEST_PROTOCOL)

	with open('matrix.txt', 'w') as f:
		f.write(json.dumps(matrix))





if __name__ == '__main__':
	load_resource()
	build_bag_of_word()