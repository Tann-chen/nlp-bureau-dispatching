import os
import csv
import json
import re
import traceback
import pickle
import requests
from bs4 import BeautifulSoup


def count_token_frequency(iid, inverse_index_value):
	flag = True
	for ele in inverse_index_value:
		if iid == ele[0]:  # ele[0] is instance id
			ele[1] = ele[1] + 1  # ele[0] is token frequency
			flag = False
			break
	if flag: # first count
		temp = [0] * 2
		temp[0] = iid
		temp[1] = 1
		inverse_index_value.append(temp)


file_path = "../data/8w_trainset.csv"
output_file_prefix = "tfidf_"
source_file = open(file_path, 'r', encoding='gb18030')
reader = csv.reader(source_file)


regexp_number = re.compile('^[0-9a-zA-Z]*$')
regexp_punct = re.compile("^[\s+\!\/_,$%^*(+\"\')]+|[:：+——()?【】“”！，。？、~@#￥%……&*（）. 〉《 》〔〕；～ ％]$")
stop_words_lst = ["市民", "来电", "咨询", "反映", "职能", "规定", "局", "内容", "工单", "问题"]
NI_suffix_tuple = ("局", "队", "所", "会", "中心", "部门")

inverse_index = {}
instance_labels = {}
instance_tokens = {}


for row in reader:
	instance_id = row[0]
	label = row[9]
	content = row[6]

	class_1 = row[2]
	class_2 = row[3]
	class_3 = row[4]
	class_4 = row[5]

	if instance_id.strip() == "ID":  # rm title
		continue

	# build request
	payload = {}
	payload['s'] = content
	payload['f'] = 'xml'
	payload['t'] = 'ner'
	response = requests.post("http://127.0.0.1:12345/ltp", data=payload, timeout=5)
	soup = BeautifulSoup(response.text, 'html.parser')
	word_tags = soup.findAll('word')
	# parse and extract features
	buffers = []
	tokens = []

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
		if pos not in ('Ni', 'n', 'j'):  # Ns exclusive
			print("[INFO] exclusive :" + token + ":" + pos)   # throw out

		elif token in inverse_index.keys(): # already in inverse index
			instances_list = inverse_index[token]
			count_token_frequency(instance_id, instances_list)
			# record tokens
			tokens.append(token)
			print("[INFO] add :" + token)
		else:
			new_list = []
			count_token_frequency(instance_id, new_list)
			inverse_index[token] = new_list
			# record tokens
			tokens.append(token)
			print("[INFO] add :" + token)

	instance_labels[instance_id] = label
	instance_tokens[instance_id] = tokens
	print("-----------------------------")


print("================ END =================")
print("totoal dimension :" + str(len(list(inverse_index.keys()))))
print("total instance :" + str(len(list(instance_tokens.keys()))))


with open(output_file_prefix + 'inverse_index.pickle', 'wb') as f:
	pickle.dump(inverse_index, f, pickle.HIGHEST_PROTOCOL)

with open(output_file_prefix + 'instance_label.pickle', 'wb') as f:
	pickle.dump(instance_labels, f, pickle.HIGHEST_PROTOCOL)

with open(output_file_prefix + 'instance_tokens.pickle', 'wb') as f:
	pickle.dump(instance_tokens, f, pickle.HIGHEST_PROTOCOL)