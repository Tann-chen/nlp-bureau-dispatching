import os
import re
import requests
import pickle
import csv
from bs4 import BeautifulSoup
from sklearn.externals import joblib


regexp_number = re.compile('^[0-9a-zA-Z]*$')
regexp_punct = re.compile("^[\s+\!\/_,$%^*(+\"\')]+|[:：+——()?【】“”！，。？、~@#￥%……&*（）. 〉《 》〔〕；～ ％]$")
stop_words_lst = ["市民", "来电", "咨询", "反映", "职能", "规定", "局", "内容", "工单", "问题"]
NI_suffix_tuple = ("局", "队", "所", "会", "中心", "部门")

global inverse_index
global nb_classfier
global agency_label_mapping

with open("bow/trainset_bow_inverse_index.pickle", 'rb') as f:
	inverse_index = pickle.load(f)

# label and agency name mapping
with open("../label_modifier/all_label.conf", 'r') as f:
	agency_label_mapping = dict()
	config_content = f.read()
	config_list = config_content.split('\n')
	for conf in config_list:
		conf_agency = conf.split(',')[0]
		label = int(conf.split(',')[1])
		agency_label_mapping[label] = conf_agency


nb_classfier = joblib.load('nb_bureau_disp_classifier.joblib')



def extract_tokens(content):
	# build request
	payload = dict()
	payload['s'] = content
	payload['f'] = 'xml'
	payload['t'] = 'ner'
	response = requests.post("http://127.0.0.1:12345/ltp", data=payload, timeout=5)
	soup = BeautifulSoup(response.text, 'html.parser')
	word_tags = soup.findAll('word')
	# parse and extract features
	buffers = list()
	tokens = list()

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
			print("[INFO] exclusive :" + token + ":" + pos)   # print, but throw out
		else:
			tokens.append(token)
			print("[INFO] add :" + token)

	return tokens


def get_pred_bow_vector(tokens):
	dimension = list(inverse_index.keys())
	vector = []
	for d in dimension:
		if d in tokens:
			vector.append(1)
		else:
			vector.append(0)

	return vector


def pred_label(content):
	tokens = extract_tokens(content)
	vector = [ get_pred_bow_vector(tokens) ]
	pred_label = nb_classfier.predict(vector)[0]
	return agency_label_mapping[pred_label]


def batch_pred(file_path):
	source_file = open(file_path, 'r')
	target_file = open('pred_result.csv', 'w', newline='')
	reader = csv.reader(source_file)
	writer = csv.writer(target_file)

	try:
		count = 0
		for row in reader:
			if row[0] == '工单编号':
				writer.writerow(row)
			else:
				content = row[1]
				pred = pred_label(content)
				row.append(pred)
				writer.writerow(row)
				count += 1
				if count == 20000:
					break

	except csv.Error as e:
		source_file.close()
		target_file.close()
		print("[ERROR]")


if __name__ == '__main__':
	#print(pred_label('龙昆南海德路昌茂花园旁边工地在超时施工，产生噪音，严重影响居民休息，请城管核实处理！谢谢！（请职能局按规定在30分钟内联系市民，响应处置）'))
	batch_pred('../data/12345wolabel.csv')






