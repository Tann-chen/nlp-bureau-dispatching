import math
import pickle
import time
import random


index_file = "tfidf_inverse_index.pickle"
instance_tokens_file = "tfidf_instance_tokens.pickle"

global tfidf_inverse_index
global tfidf_log_inversed_df
global tfidf_dimen_tokens
global tfidf_dimen_order


print("[INFO] tfidf model loading...")
with open(index_file, 'rb') as iif:
	tfidf_inverse_index = pickle.load(iif)

with open(instance_tokens_file, 'rb') as itf:
	instance_tokens = pickle.load(itf)

# tf-idf = log（1 + F(t,d)) * log(N / df) : N is number of total instances
tfidf_dimen_tokens = list(tfidf_inverse_index.keys())
num_instances = len(instance_tokens.keys())

tfidf_log_inversed_df = [0] * len(tfidf_dimen_tokens)  # cache log(N / df)

for i in range(0, len(tfidf_dimen_tokens)):
	token = tfidf_dimen_tokens[i]
	tfidf_log_inversed_df[i] = math.log( num_instances / len(tfidf_inverse_index[token]) )

del num_instances
del instance_tokens
print("[INFO] tfidf trainset model loaded.")


# load instance tokens cache for test set
global testset_instance_tokens

test_instance_tokens_file = "testset_instance_tokens.pickle"
with open(test_instance_tokens_file, 'rb') as itf:
	testset_instance_tokens = pickle.load(itf)


# shuffle order of dimension
tfidf_dimen_order = list(range(0, len(tfidf_dimen_tokens)))
random.shuffle(tfidf_dimen_order)


def get_instance_tfidf_vector(instance_id, if_shuffled=False):
	# tf-idf = log（1 + F(t,d)) * log(N / df) : N is number of total instances
	vector = [0] * len(tfidf_dimen_tokens)

	for i in range(0, len(tfidf_dimen_tokens)):
		idf = tfidf_log_inversed_df[i]  # get log (N / df) for cache
		# get F(t,d)
		tf = 0
		inverse_index_value = tfidf_inverse_index[tfidf_dimen_tokens[i]]
		# find tf
		for ele in inverse_index_value:
			if ele[0] == instance_id:
				tf = ele[1]
				break
		# calculate tf-idf
		vector[i] = math.log( 1 + tf) * idf

	if if_shuffled:
		# shuffle dimension
		shuffled_vector = []
		for i in tfidf_dimen_order:
			shuffled_vector.append(vector[i])
		return shuffled_vector
	else:
		return vector


def get_testset_instance_tfidf_vector(instance_id, if_shuffled=False):
	if instance_id not in testset_instance_tokens.keys():
		print("[ERROR] instance_id is invalid")

	# get tokens in instace
	tokens = testset_instance_tokens[instance_id]

	# tf-idf = log（1 + F(t,d)) * log(N / df) : N is number of total instances
	vector = [0] * len(tfidf_dimen_tokens)

	for i in range(0, len(tfidf_dimen_tokens)):
		idf = tfidf_log_inversed_df[i]  # get log (N / df) for cache
		
		# get F(t,d)
		tf = 0
		token = tfidf_dimen_tokens[i]
		for t in tokens:
			if t == token :
				tf += 1

		# calculate tf-idf
		vector[i] = math.log( 1 + tf) * idf

	if if_shuffled:
		# shuffle dimension
		shuffled_vector = []
		for i in tfidf_dimen_order:
			shuffled_vector.append(vector[i])
		return shuffled_vector
	else:
		return vector








