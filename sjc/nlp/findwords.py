import pandas as pd

csv=pd.read_csv("/Users/sunjincheng/Documents/nlpdata/departments.csv",encoding='gb18030')
csv2=pd.read_csv("/Users/sunjincheng/Documents/nlpdata/new.csv")
for i in range(0,csv.shape[0]):
    x=csv.loc[i]['0']
    if(i/10000==0):
        print(i)
    if(x=='纪委(监察局)' or x=='纪委'):
        print(i)
        print(csv2.loc[i]['处置单位'])

