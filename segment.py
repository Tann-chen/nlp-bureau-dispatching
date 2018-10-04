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


for row in reader:
	payload = {}
	payload['s'] = row[7]
	payload['f'] = 'xml'
	payload['t'] = 'ws'
	response = requests.post("http://127.0.0.1:12345/ltp", data=payload)
	soup = BeautifulSoup(response.text, 'html.parser')
	word_tags = soup.findAll('word')
	tokens = []
	for w in word_tags:
		token = w['cont']
		if regexp_number.match(token.strip()):
			print("[INFO] invalid token : alphnum")
		elif regexp_punct.match(token.strip()):
			print("[INFO] invalid token : punctuation_zh")
		else:
			tokens.append(token)
	doc_id = row[0]
	saved_data = saved_data + doc_id + '  ' + ','.join(tokens) + '\n'

with open('segment.txt', 'w') as file:
	file.write(saved_data)



	