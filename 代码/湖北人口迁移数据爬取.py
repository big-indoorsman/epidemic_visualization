import requests
import json
import time
import pandas as pd
from ChineseAdminiDivisionsDict import CitiesCode, ProvinceCode

areaname='湖北省'
classname='province'
no=420000
mukous = ['in','out']
for direction in mukous:
    dataframe = pd.DataFrame()
    if no == -1 :
        no = CitiesCode[str(areaname)]

    if direction == 'in' :
        nameofdire = '迁入'
    if direction == 'out':
        nameofdire = '迁出'
    CitiesOrder = {}

    times = 1
    for key , value in CitiesCode.items():
        CitiesOrder[str(key)] = times
        times += 1
    datelist = []
    counter_data = 2
    for date3 in range(20200201,20200230):
        datelist.append(date3)
    for date in datelist:
        url=f'http://huiyan.baidu.com/migration/cityrank.jsonp?dt={classname}&id={no}&type=move_{direction}&date={date}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}

        print(url)
        response=requests.get(url,headers=headers, timeout=5)
        r=response.text[3:-1]
        data_dict=json.loads(r)
        if data_dict['errmsg']=='SUCCESS':
            data_list=data_dict['data']['list']
            time.sleep(1)
            city_name=[]
            value=[]
            province_name=[]
            for i in range (len(data_list)):
                city_name.append(data_list[i]['city_name'])
                value.append(data_list[i]['value'])
                province_name.append(data_list[i]['province_name'])
            date=str(date)[-4:]
            if direction == 'in' :
                dataframe['迁入省份'] = province_name
                dataframe['迁入城市']=city_name
            else:
                dataframe['迁出省份'] = province_name
                dataframe['迁出城市'] = city_name
            dataframe[date] = value
            counter_data += 1
    dataframe.to_csv("湖北人口"+nameofdire+"情况.csv", index=False, sep=',')

