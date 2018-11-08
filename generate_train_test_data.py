import os
import csv
import json
import traceback
import random


original_file_path = "company.csv"
trainset_file_path = "original_trainingset.csv"
testset_file_path = "original_testset.csv"


try:
    source_file = open(original_file_path, 'r', encoding='gb18030')
    trainset_file = open(trainset_file_path, 'w', encoding='gb18030', newline='')
    testset_file = open(testset_file_path, 'w', encoding='gb18030', newline='')

    reader = csv.reader(source_file)
    trainset_writer = csv.writer(trainset_file)
    testset_writer = csv.writer(testset_file)
    
    for row in reader:
        if random.randint(1, 10) > 8:
            testset_writer.writerow(row) #20 percent to testset
        else:  # 80 percent to training set
            trainset_writer.writerow(row)
        
except csv.Error as e:
    source_file.close()
    target_file.close()
    print("[ERROR]")
    traceback.print_exc()
