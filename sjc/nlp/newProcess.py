import pandas as pd
import time
import re
import requests
from bs4 import BeautifulSoup
import profile


# Datafreme越小处理起来越快，可以提取部分列，处理完再合并
# 每次调用分词api耗时0.006s左右，因为数据重复率高，可以先排序，处理过程中通过判断是否与前项一样决定是否调用api
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
    if (len(ns) == 0 and sentence[1]!="委" and sentence[1]!="政" ):
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
    return sentence, '，'.join(ns)


def loadcsv(path):
    csvfile = pd.read_csv(path, encoding="gb18030")
    newcsv = csvfile[['工单编号', '处置单位']]

    # csvfile.sort_values()
    return newcsv


def cleandata(csvfile):
    newcsv = []
    predept = ''
    preloc = ''
    preline = 'null'
    print("数据总数：" + str(csvfile.shape[0]), file=doc)
    time1 = time.time()
    for i in range(0, csvfile.shape[0]):
        if (i % 1000 == 1):
            timei = time.time()
            print(str(100 * i / csvfile.shape[0]) + '%')
            print('耗时：' + str(timei - time1))
            print('剩余时间：' + str((timei - time1) * ((csvfile.shape[0] - i) / i)))
        line = (csvfile.loc[i]['处置单位'])
        gonghao = csvfile.loc[i]['工单编号']
        # if (pd.isnull(line)):
        #     continue
        # elif (line['处置单位'] == "其他单位" or line['处置单位'] == "省外单位" or line['处置单位'] == "省级单位" or line['处置单位'] == "除海口外的市县"):
        #     continue
        # sentence = line
        # if(i>=1 and sentence==csvfile.loc[i-1]['处置单位']):
        #     linepre=csvfile.loc[i-1]
        #     line['处置单位']=linepre['处置单位']
        #     line['地点']=linepre['地点']
        # else:
        #     department, location = hgdProcess(sentence)
        #     line['处置单位'] = department
        #     line['地点'] = location
        if (line == preline):
            department = predept
            location = preloc
        else:
            department, location = hgdProcess(line)

        # line['处置单位'] = department
        # line['地点'] = location
        # csvfile.loc[i]['单位']=department
        # csvfile.loc[i]['地点']=location
        newcsv.append([gonghao, line, location, department])
        preline = line
        predept = department
        preloc = location

    return newcsv


def sortdep(dep_type):
    department = []

    dep_num = set(dep_type)
    print("部门数量：" + str(len(dep_num)))
    for line in dep_num:
        department.append([line, dep_type.count(line)])
    department.sort(key=lambda x: x[1])
    前138 = 0
    for i in range(0, len(department)):
        if (i <= 135):
            前138 = 前138 + int(department[i][1])

        print(department[i][0] + ',' + str(department[i][1]), file=doc)
    print(department[135][1])
    print('总数=' + str(前138))
    return department


if __name__ == '__main__':
    doc = open("/Users/sunjincheng/Documents/nlpdata/数据总数.txt", 'w', encoding="gb18030")
    timer = time.time()
    csvfile = loadcsv("/Users/sunjincheng/Documents/nlpdata/valid_data_all.csv")
    newcsv = cleandata(csvfile)
    newcsv = pd.DataFrame(newcsv, columns=['工号', '处置单位', '地点', '单位'])
    newcsv.to_csv("/Users/sunjincheng/Documents/nlpdata/精炼版.csv", encoding='gb18030')


    # departments, locations = cleandata(csvfile)
    # sortdep(departments)
    # csvdept = pd.DataFrame(departments)
    # csvloc = pd.DataFrame(locations)
    # csvdept.to_csv("/Users/sunjincheng/Documents/nlpdata/departments.csv", encoding='gb18030')
    # csvloc.to_csv("/Users/sunjincheng/Documents/nlpdata/locations.csv", encoding='gb18030')
    # after = time.time()
    # print(after - timer)
    # doc.close()
