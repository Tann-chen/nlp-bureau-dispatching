import os
import csv
import json
import re
import traceback
import random
import requests
import pickle
import math
from bs4 import BeautifulSoup


original_file_path = "data/original_trainingset.csv"
target_file_path = "data/8w_trainset.csv"

global agency_class


def get_label(agency_name):
    label = -1
    for idx in range(0, 5):
        agency_list = agency_class[idx]
        if agency_name in agency_list:
            label = idx
            break

    if label == -1:
        print("[INFO] invalid label :" + agency_name)

    return label


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
                sentence = re.sub(word['cont'], '', sentence)
                ns.append(word['cont'])
            if (re.sub("海口", '', word['cont']) != word['cont']):
                ns.clear()
                ns.append("海口市")
    if (len(sentence) > 2 and sentence[2] == "区"):
        ns.append(sentence[0:3])
        sentence = re.sub(sentence[0:3], "", sentence)
    if (len(sentence) > 2 and re.sub("街道办", '', sentence) != sentence):
        diming = re.sub("街道办", '', sentence)
        if (diming != ''):
            ns.append(diming)
        sentence = re.sub(diming, '', sentence)
    if (len(ns) == 0 and sentence[1]!="委" and sentence[1]!="政"):
        sentence = re.sub('市', "", sentence)
    sentence = re.sub('分公司', "", sentence)
    if (sentence == "政府" or sentence == "镇政府"):
        sentence = "人民政府"
    elif (re.sub("镇政府", "", sentence) != sentence):
        sentence = "人民政府"
        ns.append(re.sub("镇政府", "", sentence))
    elif (sentence == "委办" or sentence == "委"):
        sentence = "市委办公室"
    elif (sentence == "片区棚户区（）改造项目指挥部"):
        sentence = "棚户区改造项目指挥部"
    elif (re.sub("棚改指挥部","",sentence)!=sentence):
        sentence = "棚户区改造项目指挥部"
        ns.append(re.sub("棚改指挥部","",sentence))
    elif (sentence == "纪委" or sentence == "纪委(监察局)"):
        sentence = "纪委监察局"
    elif (sentence == "省外单位" or sentence == "无效归属"):
        sentence = "无效数据"
    elif (sentence == "面前坡片区改造项目指挥部"):
        sentence = "改造项目指挥部"
        ns.append('面前坡片区')
    elif(re.sub("组织部","",sentence)!=sentence):
        sentence = "组织部"
    elif(sentence=='中国国民党革命委员会委员会'):
        sentence="中国国民党革命委员会"
    elif(sentence=='残联'):
        sentence='残疾人联合会'
    elif(sentence=='城管局'):
        sentence='城市管理行政执法局'
    elif(sentence=='住建局'):
        sentence="住房和城乡建设局"
    elif(sentence=='物价局'):
        sentence='物价监督局'
    elif (sentence == '园林局'):
        sentence = '园林管理局'
    elif (sentence == '国资'):
        sentence = '国土资源局'
    elif (sentence == '人社局'):
        sentence = '人力资源和社会保障局'
    elif (sentence == '科工信局'):
        sentence = '科学技术工业信息化局'

    return sentence


if __name__ == '__main__':
    with open("label.conf", 'r') as file:
        labeled_agencies = file.read()
        labeled_agencies_list = labeled_agencies.split('\n')
        agency_class = []
        for i in range(0, 5):
            agency_class.append([])
        
        for a in labeled_agencies_list:
            if len(a) == 0:
                continue
            agency_name = a.split(',')[0]
            label_class = a.split(',')[1]
            agency_class[int(label_class)].append(agency_name)

    try:
        source_file = open(original_file_path, 'r', encoding='gb18030')
        target_file = open(target_file_path, 'w', encoding='gb18030', newline='')
        reader = csv.reader(source_file)
        writer = csv.writer(target_file)
        # write title
        writer.writerow(["ID", "工单编号", "行业分类1级", "行业分类2级", "行业分类3级", "行业分类4级", "诉求内容", "原处置单位", "处置单位", "单位类别"])
        invalid_agency = ["其他单位", "省外单位", "除海口外的市县", "无效归属", "省级单位", "处置单位"]

        docu_id = -1
        required_num = 80000
        
        #
        #label_count = [0] * 5

        for row in reader:
            docu_id += 1

            if random.randint(1, 10) > 7:
                print("[INFO] pass id :" + str(docu_id))
                continue

            if  len(row[12]) == 0 or row[12] in invalid_agency:
                print("[INFO] invalid data")
                continue

            dealed_agency_name = hgdProcess(row[12])
            label = get_label(dealed_agency_name)

            if label == -1:
                continue

            # # 
            # if label_count[int(label)] >= 800:
            #     print("[INFO] some label data overflow :" + str(label))
            #     continue 
            # #
            # label_count[int(label)] = label_count[int(label)] + 1

            new_list = []
            new_list.append(docu_id)
            new_list.append(row[0])
            new_list.append(row[2])
            new_list.append(row[3])
            new_list.append(row[4])
            new_list.append(row[5])
            new_list.append(row[7])
            new_list.append(row[12])
            new_list.append(dealed_agency_name)
            new_list.append(label)

            writer.writerow(new_list)
            required_num -= 1

            if required_num == 0:
                print("-------- END ---------")
                break

    except csv.Error as e:
        source_file.close()
        target_file.close()
        print("[ERROR]")
        traceback.print_exc()
