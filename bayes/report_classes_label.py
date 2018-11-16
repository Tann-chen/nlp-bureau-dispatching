import pickle

with open("classes_list.pickle", 'rb') as iif:
	classes_list = pickle.load(iif)

classes = classes_list[3]
label = -1
string = ""

for c in classes:
	label += 1
	c = c.replace("‘", "")
	string = string + c +" " + str(label) + "; "

print(string)

	
