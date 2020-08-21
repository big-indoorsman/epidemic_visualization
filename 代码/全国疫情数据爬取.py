import requests
import json
import pandas as pd
url_1 ='https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
res_1=requests.get(url_1,headers = headers)
d=json.loads(res_1.text)
data_all=json.loads(d['data'])
all_data = {}
for i in list(data_all['provinceCompare'].keys()):
    url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province={0}'.format(i)
    response = requests.post(url,headers = headers)
    data = json.loads(response.text)['data']
    date=[]
    province=[]
    confirm=[]
    dead=[]
    heal=[]
    index=[]
    for i in data:
        if i['date']=='03.01' :
            index=data.index(i)
    for num in range(index,index+31):
        date.append(data[num]['date'])
        province.append(data[num]['province'])
        try:
            confirm.append(data[num]['confirm'])
        except:
            confirm.append(0)
        try:
            dead.append(data[num]['dead'])
        except:
            dead.append(0)
        try:
            heal.append(data[num]['heal'])
        except:
            heal.append(0)
    if province[0]=='上海':
        dataframe = pd.DataFrame({'date':date,'province':province,'confirm':confirm,'dead':dead,'heal':heal})
        dataframe.to_csv("全国疫情情况.csv",index=False,sep=',')
    else:
        dataframe = pd.DataFrame({'date':date,'province':province,'confirm':confirm,'dead':dead,'heal':heal})
        dataframe.to_csv("全国疫情情况.csv",index=False,sep=',',header=False,mode='a')