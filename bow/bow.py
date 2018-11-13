import os
import csv
import json
import re
import traceback
import pickle
import requests
from bs4 import BeautifulSoup


global inverse_index

with open("bow_inverse_index.pickle", 'rb') as iif:
	inverse_index = pickle.load(iif)


def get_bag_of_word_vector(instance_id):
	vector = []
	for token, iid_set in inverse_index.items():
		if instance_id in iid_set:
			vector.append(1)
		else:
			vector.append(0)

	return vector



if __name__ == '__main__':
	print(get_bag_of_word_vector(''))