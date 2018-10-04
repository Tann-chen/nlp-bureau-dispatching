import os
import pickle
import numpy
import re
import string
from sklearn import linear_model



segment_file = 'segment_description.pickle'
selected_depart = '市公安局'

regexp_number = re.compile('^[0-9a-zA-Z]*$')
regexp_punct = re.compile("^[\s+\!\/_,$%^*(+\"\')]+|[:：+——()?【】“”！，。？、~@#￥%……&*（）. 〉《 》〔〕；～ ％]$")

punctuations = set(string.punctuation)

with open(segment_file, 'rb') as file:
	segmented_lst = pickle.load(file)
	token_set = set()
	counter = 0
	# build features dimension 
	for r in segmented_lst:
		segmented_description = r['seg_description']
		temp_tokens_lst = segmented_description.split('/')
		for t in temp_tokens_lst:
			if regexp_number.match(t.strip()):
				print("[INFO] invalid token : alphnum")
			elif regexp_punct.match(t.strip()):
				print("[INFO] invalid token : punctuation_zh")
			elif t.strip() in punctuations:
				print("[INFO] ivalid token : punctuation_en")
			else:
				token_set.add(t.strip())

	feature_tags = list(token_set)
	feature_tags.sort()
	print(feature_tags)
	with open('features.txt', 'w') as file:
		file.write(','.join(feature_tags))


	generate the trained data for linear
	matrix = []
	tags_lst = []

	for r in segmented_lst:
		segmented_description = r['seg_description']
		description_tokens_lst = segmented_description.split('/')
		description_tokens_lst.sort()
		description_tokens_lst = [t.strip() for t in description_tokens_lst if not regexp_number.match(t.strip()) and t.strip() not in punctuations]

		# to reduce complxity of matching, match betweeen two sorted list
		features_idx = 0
		des_token_idx = 0
		r_feature = [0] * len(feature_tags)

		for t in description_tokens_lst:
			for i in range(0, len(feature_tags)):
				if feature_tags[i] == t:
					r_feature[i] = 1


		while(des_token_idx < len(description_tokens_lst) and features_idx < len(feature_tags)):
			if(feature_tags[features_idx] == description_tokens_lst[des_token_idx]):
				r_feature[features_idx] = 1
				des_token_idx = des_token_idx + 1
			features_idx = features_idx + 1

		matrix.append(r_feature)
		if r['place'] == selected_depart:
			tags_lst.append(1)
		else:
			tags_lst.append(0)

	# linear regression
	linear_reg = linear_model.LinearRegression()
	linear_reg.fit(matrix, tags_lst)
	LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None, normalize=False)
	print(linear_reg.coef_)








