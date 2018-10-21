import os
import csv
import json
import traceback
import pandas

original_file_path = "/Users/sunjincheng/Documents/nlpdata/valid_data_all.csv"
target_file_path = "/Users/sunjincheng/Documents/nlpdata/5000new.csv"
top_lines = 5000

try:
    source_file = open(original_file_path, 'r', encoding='gb18030')
    target_file = open(target_file_path, 'w', encoding='gb18030', newline='')
    reader = csv.reader(source_file)
    writer = csv.writer(target_file)
    for row in reader:
        top_lines = top_lines - 1
        writer.writerow(row)
        if(top_lines == 0):
            break


except csv.Error as e:
    source_file.close()
    target_file.close()
    print("[ERROR]")
    traceback.print_exc()
