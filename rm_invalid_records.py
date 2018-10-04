import os
import csv
import json
import traceback

source_file_path = "top5000.csv"
target_file_path = "valid5000.csv"
invalid_handlers_lst = ['其他单位', '省外单位', '省级单位', '处置单位']
counter = 0
qita_counter = 0
null_counter = 0
shengji_counter = 0
shengwai_counter = 0
chuzhi_counter = 0

try:
    source_file = open(source_file_path, 'r', encoding='gb18030')
    target_file = open(target_file_path, 'w', encoding='gb18030', newline='')
    reader = csv.reader(source_file)
    writer = csv.writer(target_file)

    for row in reader:
        class_1 = row[2]
        class_2 = row[3]
        class_3 = row[4]
        class_4 = row[5]
        title = row[6]
        content = row[7]
        handler = row[12].strip()
        if(len(handler) > 0 and handler not in invalid_handlers_lst):
            writer.writerow(row)
            counter = counter + 1
        elif len(handler) == 0:
            null_counter  = null_counter + 1
        elif handler == '其他单位':
            qita_counter = qita_counter + 1
        elif handler == '省外单位':
            shengwai_counter = shengwai_counter + 1
        elif handler == '省级单位':
            shengji_counter = shengji_counter + 1
        elif handler == '处置单位':
            chuzhi_counter = chuzhi_counter + 1
        else :
            print("DEBUG")

except csv.Error as e:
    source_file.close()
    target_file.close()
    print("[ERROR]")
    traceback.print_exc()

print("-------- DONE --------")
print("valid records : " + str(counter))
print("null records : " + str(null_counter))
print("其他单位 : " + str(qita_counter))
print("省外单位 : " + str(shengwai_counter))
print("省级单位 : " + str(shengji_counter))
print("处置单位 : " + str(chuzhi_counter))
