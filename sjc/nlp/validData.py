import csv
import pandas as pd
import time
import re
import requests
from bs4 import BeautifulSoup

def hgdProcess(sentence):
    payload = {}
    payload['s'] = sentence
    payload['f'] = 'xml'
    payload['t'] = 'pos'
    ns = []
    response = requests.post("http://127.0.0.1:12345/ltp", data=payload)
    # docker run -d -p 12345:12345 ce0140dae4c0 ./ltp_server --last-stage all
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    word_tags = soup.findAll('word')
    # for word in word_tags:
    #     word = word['cont']
    for word in word_tags:
        if (word['pos'] == 'ns'):
            if (word['cont'] != "中国"):
                sentence = re.sub(word['cont'],'', sentence)
            ns.append(word['cont'])
    if (len(sentence) > 2 and sentence[2] == "区"):
        ns.append(sentence[0:3])
        sentence = re.sub(sentence[0:3], "", sentence)
    if (len(sentence) > 2 and re.sub("街道办", '', sentence) != sentence):
        diming = re.sub("街道办", '', sentence)
        if(diming!=''):
            ns.append(diming)
        sentence = re.sub(diming,'',sentence)
    return sentence, '，'.join(ns)

file_path = "/Users/sunjincheng/Documents/nlpdata/5000new.csv"
time1=time.clock()
csv_data = pd.read_csv(file_path, encoding="gb18030")  # 读取训练数据
csv_data.sort_values(by='处置单位')
csv_data.insert(12,'地点',None)
time2=time.clock()
print(csv_data.shape)
print("加载csv耗时："+str(time2-time1))
valid_data = []
null_data = []
nonvalid_data = []
dep_type = []
department = []
print("数据行数："+str(csv_data.shape[0]))

for i in range(0, csv_data.shape[0]):
    line = (csv_data.loc[i])
    if (pd.isnull(line['处置单位'])):
        nonvalid_data.append(line)
    elif (line['处置单位'] == "其他单位" or line['处置单位']=="省外单位" or line['处置单位'] == "省级单位" or line['处置单位'] == "除海口外的市县" or line['处置单位'] =='无效归属'):
        nonvalid_data.append(line)
    # else:
    #     line2=line['处置单位']
    #     hgdline=hgdProcess(line2)
    #     location=hgdline[1]
    #     sentence=hgdline[0]
    #
    #     if (len(hgdline[1]) == 0):
    #         line['处置单位'] = re.sub("市", "", line['处置单位'])
    #     else:
    #         line['处置单位'] = re.sub("分公司", "", sentence)
    #
    #     # print(line['处置单位'])
    #     if(len(location)>1 and location[len(location)-2]+location[len(location)-1]=='海口'):
    #         line['地点'] = '海口市'
    #     else:
    #         line['地点'] = location
    #
    #     if(line['处置单位'] == "镇政府" or line['处置单位'] == "政府"):
    #         line['处置单位'] = "人民政府"

        valid_data.append(line)


        dep_type.append(line['处置单位'])
time3=time.clock()
valid_num = len(valid_data)
print("数据处理时间："+str(time3-time2))
# null_num=len(null_data)

print("有效数据：" + str(valid_num))
print('无效数据：' + str(len(nonvalid_data)))

valid_df = pd.DataFrame(valid_data)
nonvalid_df=pd.DataFrame(nonvalid_data)
# 排列


valid_df = valid_df.sort_values(by='处置单位')
nonvalid_df=nonvalid_df.sort_values(by='处置单位')

valid_df.to_csv('/Users/sunjincheng/Documents/valid_data_all.csv', encoding="gb18030")
nonvalid_df.to_csv('/Users/sunjincheng/Documents/nonvalid_all.csv', encoding="utf-8")

dep_num = set(dep_type)

print("部门数量：" + str(len(dep_num)))
time4=time.clock()
for line in dep_num:
    department.append([line,dep_type.count(line)])
department.sort(key=lambda x:x[1])
for i in range(0,len(department)):
    print(department[i][0]+str(department[i][1]))


