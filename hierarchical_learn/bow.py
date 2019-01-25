import os
import csv
import json
import re
import traceback
import pickle
import requests
from bs4 import BeautifulSoup


with open("../bayes/bow/01234/trainset_bow_inverse_index.pickle", 'rb') as iif:
	inverse_index = pickle.load(iif)

with open("../bayes/bow/test_zkall/testset_bow_instance_tokens.pickle", 'rb') as itf:
	testset_instance_tokens = pickle.load(itf)



def get_testset_bow_vector(instance_id):
	global inverse_index
	global testset_instance_tokens

	if instance_id not in testset_instance_tokens.keys():
		print("[ERROR] instance id is not invalid")
	else:	
		tokens = testset_instance_tokens[instance_id]
		dimension = list(inverse_index.keys())
		vector = []
		for d in dimension:
			if d in tokens:
				vector.append(1)
			else:
				vector.append(0)

		return vector