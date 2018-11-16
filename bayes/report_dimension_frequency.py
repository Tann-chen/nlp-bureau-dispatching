import pickle
import matplotlib.pyplot as plt


with open("bow_inverse_index.pickle", 'rb') as iif:
	inverse_index = pickle.load(iif)

x = list(range(1,51))
y = []

for fre in range(1, 51):
	count = 0
	for token, docu_list in inverse_index.items():
		if len(docu_list) == fre:
			count += 1
	print(count)
	y.append(count)


# fre >= 50 
count = 0
for token, docu_list in inverse_index.items():
	if len(docu_list) > 50:
		count += 1
print(count)
y.append(count)

X = ['1', '2-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-40','41-45', '46-50', '>50']
Y = []

Y.append(y[0])
Y.append(y[1]+ y[2] + y[3] + y[4])

for i in range(6, 50, 5):
	Y.append(y[i-1] + y[i] + y[i+1] + y[i+2] + y[i+3])

Y.append(y[-1])
print(Y)

#plot
plt.bar(X,Y)
plt.show()


