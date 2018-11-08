from tfidf import get_instance_tfidf_vector
import time

for i in  range(0, 100):
	start = time.time()
	result  = get_instance_tfidf_vector("197", True)
	end = time.time()
	print(end - start)