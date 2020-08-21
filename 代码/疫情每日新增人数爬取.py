import requests
import json
import pandas as pd
url_1 ='https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
res_1=requests.get(url_1,headers = headers)
d=json.loads(res_1.text)
data_all=json.loads(d['data'])
confirm=[]
suspect=[]
dead=[]
heal=[]
date=[]
for i in range(len(data_all['chinaDayAddList'])):
    date.append(data_all['chinaDayAddList'][i]['date'])
    confirm.append(data_all['chinaDayAddList'][i]['confirm'])
    suspect.append(data_all['chinaDayAddList'][i]['suspect'])
    dead.append(data_all['chinaDayAddList'][i]['dead'])
    heal.append(data_all['chinaDayAddList'][i]['heal'])
dataframe = pd.DataFrame({'date':date,'confirm':confirm,'suspect':suspect,'dead':dead,'heal':heal})
dataframe.to_csv("新增人数.csv",index=False,sep=',')