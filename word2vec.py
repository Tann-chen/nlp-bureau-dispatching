import lib.synonyms
import pickle
import json
# from sklearn.cluster import KMeans
# from sklearn.decomposition import PCA

# file_path = "agency_data.txt"
# source_file = open(file_path, 'r', encoding='gb18030')

# print(synonyms.seg("精神文明建设指导委员会办公室"))
# print(synonyms.nearby("统计局"))

NI_ends_one = ('局', '社','委', '办')
NI_ends_two = ('大队', '支队','中心')

with open("agency.txt", 'r', encoding='gb18030') as f:
	data = f.read()

agency_2_vec = {}

agency_lst = data.split('\n')
for row in agency_lst:
	agency_name = row.split(',')[0]
	print("[NEW] " + agency_name + "is handling")
	if len(agency_name.strip()) == 0:
		continue

	vector = []
	if_exception = False

	try:
		vector = list(synonyms.v(agency_name))
	except KeyError:
		print("[INFO] origin agency name not in vocabulary :" + agency_name)
		if_exception = True

	if if_exception:
		if agency_name.endswith(NI_ends_one):
			print("[WARN] change agency_name from : " + agency_name + " to: " + agency_name[:-1])
			agency_name_modified = agency_name[:-1]
		if agency_name.endswith(NI_ends_two):
			print("[WARN] change agency_name from : " + agency_name + " to: " + agency_name[:-2])
			agency_name_modified = agency_name[:-2]

		segment_lst = synonyms.seg(agency_name_modified)[0]
		print("[INFO] seg agency name to :" + str(segment_lst))
		vector = [0] * 100

		for s in segment_lst:
			temp_vector = []
			try:
				temp_vector = synonyms.v(s)
			except KeyError:
				print("[INFO] segment not in vocabulary :" + s)
			if temp_vector is not None and len(temp_vector) > 0:
				for i in range(0, 100):
					vector[i] = vector[i] + temp_vector[i]

		# get average
		for i in range(0, 100):
			vector[i] = vector[i] / len(segment_lst)


	# add to agency_2_vec
	if sum(vector) != 0:
		agency_2_vec[agency_name] = vector
	else:
		print("-----------  DEBUG :" + agency_name + "-------------")
		print(vector)


with open('agency_2_vec.pickle', 'wb') as f:
	pickle.dump(agency_2_vec, f, pickle.HIGHEST_PROTOCOL)


print("================ Result ==================")
for k,v in agency_2_vec.items():
	print(k)
	print(v)
	print("---------------------------")




