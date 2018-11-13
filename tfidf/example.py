from tfidf import get_instance_tfidf_vector
import time


start = time.time()
# params:
#  	* instance id : string
#  	* if shuffle : shuffle the order of dimensions(为了做卷积神经网络), but order of dimensions for diff instances still same 
result  = get_instance_tfidf_vector("197", True)
print(result)
end = time.time()
print(end - start)