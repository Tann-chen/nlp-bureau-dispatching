import pickle

with open("bayes/classes_list.pickle", 'rb') as iif:
	classes_list = pickle.load(iif)

print(classes_list[0])
