from snownlp import SnowNLP
import jieba
import csv
import pandas as pd
topic_data={}
with open(r'C:\Users\15503\PycharmProjects\mysite\微博疫情话题评论.csv','r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header_row = next(reader)
    topic,comment= [], []
    for row in reader:
        topic.append(row[0])
        comment.append(row[1])
words=[]
for line in comment:
    text=str(line).replace('[','').replace(']','').replace(',','').replace('\'','').replace(' ','').replace('\n','')
    seg_list = jieba.cut(text,cut_all=False)
    word=[]
    for i in seg_list:
        cut_words = SnowNLP(i).sentiments
        if cut_words==0.5:
            num=0
        elif cut_words<0.5:
            num=-1
        else:
            num=1
        word.append(num)
    words.append(word)
positive=[]
negative=[]
neutral=[]
for i in words:
    positive.append(i.count(1))
    negative.append(i.count(-1))
    neutral.append(i.count(0))
topics=['钟南山院士指导研发快速检测试剂盒','我的治愈故事','如何科学节约口罩','环保酵素不可用于消毒','铁路客座率将控制在50%左右','防控新型冠状病毒肺炎临时指南']
dataframe = pd.DataFrame({'topic':topics,'positive':positive,'negative':negative,'neutral':neutral})
dataframe.to_csv("微博疫情评论分析结果.csv",index=False,sep=',',header=True)