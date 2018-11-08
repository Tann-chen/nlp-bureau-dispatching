from tfidf_use import tfidf
import xgboost as xgb
import numpy as np
from sklearn.decomposition import PCA
import time
import data
import csv
from scipy.sparse import csr_matrix
import pickle

DEBUG = True
name_row = []
training_label = []
training_data = []
test_label = []
test_data = []
start_time = time.perf_counter()
with open('testset_with_label.csv', 'r') as db01:
    reader = csv.reader(db01)
    row_count = sum(1 for row in reader)
    db01.close()

with open('testset_with_label.csv', 'r') as db01:
    reader = csv.reader(db01)
    for i,row in enumerate(reader):
        if i == 1:
            name_row.append(row)
        elif i > 2 and i < 103:
            #get tfidf
            temp = tfidf.get_instance_tfidf_vector(str(row[0]))
            temp.extend(row[11:])

            training_label.append(int(row[10]))
            training_data.append(temp)

            del temp


#         if (row_count - i) < 4001:
#
#             temp = tfidf.get_instance_tfidf_vector(str(row[0]))
#             temp.extend(row[11:])
#
#             test_label.append(int(row[10]))
#             test_data.append(temp)
# if DEBUG:
#     print(len(test_label))

# with open('test_label.pickle', 'wb') as f:
# 	pickle.dump(test_label, f, pickle.HIGHEST_PROTOCOL)
# with open('test_data.pickle', 'wb') as f:
# 	pickle.dump(test_data, f, pickle.HIGHEST_PROTOCOL)

# Test data is last 4k data
test_label = data.read_pickle('test_label.pickle')
test_data = data.read_pickle('test_data.pickle')

test_data_array = np.array(test_data, dtype=float, ndmin=2)
test_label_array = np.array(test_label, dtype=int).reshape(4000, 1)

end_time = time.perf_counter()
print('Finish {} s'.format(end_time - start_time))
#down sample
# pca = PCA(n_components=12)
# training_data = pca.fit_transform(training_data)
#array
data = np.array(training_data, dtype=float, ndmin=2)
label = np.array(training_label, dtype=int).reshape(len(training_data),1)


del training_data

training_ratio = int(0.8 * label.shape[0])
# print(training_ratio)

train_X_array = data[:training_ratio, :]
train_Y_array = label[:training_ratio, :]
test_X_array= data[training_ratio:, :]
test_Y_array = label[training_ratio:, :]

if DEBUG:

    print(train_X_array.shape)
    print(train_Y_array.shape)
    print(test_X_array.shape)
    print(test_Y_array.shape)

# #start training
print('Start training')
xg_train = xgb.DMatrix(train_X_array, label = train_Y_array)
xg_test = xgb.DMatrix(test_X_array, label = test_Y_array)

param = {}
# use softmax multi-class classification
param['objective'] = 'multi:softmax'
# scale weight of positive examples
param['eta'] = 0.1
param['max_depth'] = 5
param['silent'] = 1
param['num_class'] = 6

watchlist = [ (xg_train,'train_1'), (xg_test, 'test') ]
num_round = 5
# model_1 = xgb.train(param, xg_train, num_round, watchlist )
# model_1.save_model('model_1.model')

#train
model_2 = xgb.train(param, xg_train, num_round, watchlist, xgb_model='model_5.model')
model_2.save_model('model_final.model')

# # get prediction
pred = model_2.predict( xg_test )
print ('predicting, classification error=%f' % (sum( int(pred[i]) != test_Y_array[i] for i in range(len(test_Y_array))) / float(len(test_Y_array)) ))
#
# param['objective'] = 'multi:softprob'
# bst = xgb.train(param, xg_train, num_round, watchlist)
# yprob = bst.predict( xg_test ).reshape( test_Y_array.shape[0], 6)
# ylabel = np.argmax(yprob, axis=1)  # return the index of the biggest pro
#
# print ('predicting, classification error=%f' % (sum( int(ylabel[i]) != test_Y_array[i] for i in range(len(test_Y_array))) / float(len(test_Y_array)) ))
#


