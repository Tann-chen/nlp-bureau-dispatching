import thulac
import jieba
import re
import sys
import jieba.analyse
import pandas as pd
import traceback
import requests
from bs4 import BeautifulSoup

# thu = thulac.thulac(seg_only=True)
sentence = "海口威立雅水务有限公司"


def cutword(sentence):
    sentence = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[a-zA-Z0-9+——！，。？、~@#￥%……&*（）《》：:]+", "",
                      sentence)
    jieba.del_word('市民')
    jieba.del_word('来电')
    jieba.del_word('市民来')
    jieba.del_word('谢谢')
    jieba.del_word('微信')
    jieba.del_word('咨询')
    key_w = jieba.analyse.extract_tags(sentence, topK=15, withWeight=False, allowPOS=('ns'))
    return ",".join(key_w)


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
#
# file_path = '/Users/sunjincheng/Documents/valid_data_5000.csv'
# csv_data = pd.read_csv(file_path, encoding="utf-8")
# df=pd.DataFrame(csv_data)
#
# key_w = jieba.analyse.extract_tags(sentence, withWeight=False, allowPOS=())
# print(key_w)
# key_w2 = jieba.analyse.extract_tags(sentence, withWeight=False, allowPOS=('ns'))
# print(key_w2)
# key_w3 = jieba.analyse.textrank(sentence,withWeight=False, allowPOS=('nt','ns'))
# print(key_w3)
# for line in csv_data['处置单位']:
#     location=hgdProcess(line)
#     print(location)

# 哈工大nlp
# for i in range(0,4998):
#     sen=df['处置单位'][i]
#     line = str(hgdProcess(df['处置单位'][i]))
#     linenocoma=re.sub(",","",line)
#     if(len(line)==0):
#         df['处置单位'][i] =re.sub("市","",sen)
#     elif(line=="海口"):
#         df['处置单位'][i] = "海口市," + re.sub(linenocoma, "", sen)
#     else:
#         df['处置单位'][i] = line+","+re.sub(linenocoma,"",sen)
#     print(df['处置单位'][i])
# df.to_csv('/Users/sunjincheng/Documents/city5000.csv', encoding="utf8")

# df['地名']=None
# for i in range(0,len(df['处置单位'])-1):
#     sen=df['处置单位'][i]
#     line = str(hgdProcess(df['处置单位'][i]))
#     linenocoma=re.sub(",","",line)
#     if(len(line)==0):
#         df['处置单位'][i] =re.sub("市","",sen)
#         df["地名"][i]="海口市"
#     else:
#         df['处置单位'][i] =re.sub(linenocoma,"",sen)
#         df['地名'][i]=line
#         if( line == '海口'):
#             df['地名'][i] = '海口市'
#     print(df['处置单位'][i])
# df.to_csv('/Users/sunjincheng/Documents/city5000.csv', encoding="gb18030")
#
