import os
import csv

source_file_path = "original_testset.csv"
source_file = open(source_file_path, 'r', encoding='gb18030')
reader = csv.reader(source_file)

count = 0

for row in reader:
	count += 1

print("total count :" + str(count))

