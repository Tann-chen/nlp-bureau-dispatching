from tfidf import get_instance_tfidf_vector
from tfidf import get_testset_instance_tfidf_vector
import time

## get tfidf vector for training set ##

# params:
#  	* instance id : string
#  	* if shuffle(default=False) : shuffle the order of dimensions(为了做卷积神经网络), but order of dimensions for diff instances still same 
result  = get_instance_tfidf_vector("197")
print(result)




## get tfidf vector for test set ##

# params:
#  	* instance id : string
#  	* if shuffle(default=False) : shuffle the order of dimensions(为了做卷积神经网络), but order of dimensions for diff instances still same 
result = get_testset_instance_tfidf_vector("81")
print(result)
