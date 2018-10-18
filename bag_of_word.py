import os
import csv
import json
import re
import traceback
import requests
from bs4 import BeautifulSoup


file_path = "valid5000.csv"
source_file = open(file_path, 'r', encoding='gb18030')
reader = csv.reader(source_file)
saved_data = ''
regexp_number = re.compile('^[0-9a-zA-Z]*$')
regexp_punct = re.compile("^[\s+\!\/_,$%^*(+\"\')]+|[:：+——()?【】“”！，。？、~@#￥%……&*（）. 〉《 》〔〕；～ ％]$")
# stop_words_lst = ["市民", "来电", "咨询", "反映"]
NI_suffix_lst = ["局", "处", "队", "所", "会"]


for row in reader:
	payload = {}
	payload['s'] = row[7]
	payload['f'] = 'xml'
	payload['t'] = 'ner'
	response = requests.post("http://127.0.0.1:12345/ltp", data=payload, timeout=5)
	soup = BeautifulSoup(response.text, 'html.parser')
	word_tags = soup.findAll('word')
	tokens = []
	buffers = []

	for w in word_tags:
		token = w['cont']
		pos = w['pos']
		ne = w['ne']

		# rm stop words
		# if token in stop_words_lst and ne is 'O':
		# 	continue

		# merge continuous nouns
		if ne.startswith('B-') or ne.startswith('I-'):
			buffers.append(token)
			continue

		if ne.startswith('E-'):
			buffers.append(token)
			token = ''.join(buffers)
			buffers.clear()

		# note the NER
		if ne is not 'O':
			pos = ne[-2:]

		# filter numbers & punct
		if regexp_number.match(token.strip()):
			print("[INFO] invalid token : alphnum")
			continue
		if regexp_punct.match(token.strip()) or pos == 'wp':
			print("[INFO] invalid token : punctuation")
			continue

		# custom rules
		if pos == 'j' and token[-1:] in NI_suffix_lst:
			pos = 'Ni'
			print("[INFO] pos of token should be Ni : " + token)
		
		tokens.append(token + '^' + pos)
	
	doc_id = row[0]
	saved_data = saved_data + doc_id + '  ' + ''.join(tokens) + '\n'

with open('pos.txt', 'w') as file:
	file.write(saved_data)



	