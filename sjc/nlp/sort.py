import pandas as pd


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

        print(department[i][0] + ',' + str(department[i][1]))
    print(department[135][1])
    print('总数=' + str(前138))
    return department

valid_data=pd.read_csv("/Users/sunjincheng/Documents/nlpdata/精炼版.csv")

dept=[]
dept=valid_data['单位'].tolist()



sortdep(dept)
