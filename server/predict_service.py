import os
import re
import requests
import pickle
from bs4 import BeautifulSoup
from sklearn.externals import joblib


regexp_number = re.compile('^[0-9a-zA-Z]*$')
regexp_punct = re.compile("^[\s+\!\/_,$%^*(+\"\')]+|[:：+——()?【】“”！，。？、~@#￥%……&*（）. 〉《 》〔〕；～ ％]$")
stop_words_lst = ["市民", "来电", "咨询", "反映", "职能", "规定", "局", "内容", "工单", "问题"]
NI_suffix_tuple = ("局", "队", "所", "会", "中心", "部门")

global inverse_index
global nb_classfier

with open("repo/trainset_bow_inverse_index.pickle", 'rb') as f:
	inverse_index = pickle.load(f)

nb_classfier = joblib.load('repo/nb_bureau_disp_classifier.joblib')


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



def pred_label_service(content):
	tokens = extract_tokens(content)
	vector = [ get_pred_bow_vector(tokens) ]
	pred_label = nb_classfier.predict(vector)
	return pred_label[0]







