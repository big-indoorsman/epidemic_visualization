import jieba
import csv
import pandas as pd
import re
topic_data={}
with open('youtube评论数据.csv','r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header_row = next(reader)
    date,comment= [], []
    for row in reader:
        date.append(row[0])
        comment.append(row[1])
from collections import Counter
results=[]
excludes=[]
with open('stop.txt') as f:
    for line in f:
        line = line.strip('\n')
        excludes.append(line)
word1=[]
nun=[]
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
for i in comments:
    i=i.replace(']','').replace('[','').replace('"','').replace('\'','').replace('/','').replace('.','').replace(',','').replace('?','').replace('!','')
    words = i.lower().split()
    dict=Counter(words)
    for word in words:
        if word in excludes:
            del(dict[word])
    p1 = []
    p2 = []
    for key in dict:
        p1.append(key)
        p2.append(dict[key])
    word1.append(p1)
    nun.append(p2)
dataframe = pd.DataFrame({'date': dates, 'word': word1,'number':nun})
dataframe.to_csv("youtube词云数据.csv", index=False, sep=',')