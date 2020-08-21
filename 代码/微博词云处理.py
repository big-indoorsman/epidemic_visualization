import jieba
import csv
import pandas as pd
import re
topic_data={}
with open('微博评论数据.csv','r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header_row = next(reader)
    date,comment= [], []
    for row in reader:
        date.append(row[1])
        comment.append(row[8])
comments=[]
dates=[]
for i in range(1,21):
    date1='6月'+str(i)+'日'
    dates.append(date1)
    start=18*(i-1)
    end=18*i-1
    data=''
    for j in range(start,end):
        data+=comment[j]
    comments.append(data)
from collections import Counter
list=[]
for i in comments:
    pattern=re.compile("[\u4e00-\u9fa5]")
    data="".join(pattern.findall(str(i)))
    data=jieba.cut(data,cut_all=False,HMM=True)
    list1=[]
    for j in data:
        if len(j)!=1:
            list1.append(j)
    list.append(list1)
results=[]
number=[]
for i in list:
    p1=[]
    p2=[]
    result = Counter(i)
    for key in result:
        p1.append(key)
        p2.append(result[key])
    results.append(p1)
    number.append(p2)
dataframe = pd.DataFrame({'date': dates, 'word': results,'number':number})
dataframe.to_csv("微博词云数据.csv", index=False, sep=',')