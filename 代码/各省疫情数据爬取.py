import re
import requests
import pandas as pd
import json
data_city={}
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
url = 'http://www.maps7.com/china_province.php'
page = requests.get(url,headers=headers)
file = page.text
for num in range(0,34):
    cities = []
    city=''
    province=''
    if (num == 33):
        one = re.findall('<a name="33"(.*)</a>', file)
    else:
        one = re.findall('<a name="' + str(num) + '" href=.*?>(.*?)<a name="' + str(num + 1) + '" href=.*?>', file)
    for i in one:
        if (num == 0):
            province = re.findall('(.*?)</a></h4>', i)
        else:
            province = re.findall('<h4>(.*?)</h4>', i)
        city = re.findall('<a href="/china/dianziditu.*?>(.*?)</a>', i)
    for i in province:
        if (len(city) != 0):
            for j in city:
                cities.append(j)
        else:
            cities.append(i)
    data_city[i.replace('省','').replace('市','')]=cities

data_city["广西"] = data_city.pop("广西壮族自治区")
data_city["新疆"] = data_city.pop("新疆维吾尔自治区")
data_city["香港"] = data_city.pop("香港特别行政区")
data_city["澳门"] = data_city.pop("澳门特别行政区")
data_city["内蒙古"] = data_city.pop("内蒙古自治区")
data_city["宁夏"] = data_city.pop("宁夏回族自治区")
for i in data_city.keys():
    for j in data_city[i]:
        ci = j
        if len(j) != 2:
            j = j.replace('市', '').replace('区', '').replace('县', '')
        url = 'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province={0}&city={1}'.format(i, j)
        response = requests.post(url, headers=headers)
        data = json.loads(response.text)['data']
        date = []
        province = []
        confirm = []
        dead = []
        province_city = []
        heal = []
        try:
            for num in data:
                if num['date'] == '03.01':
                    index = data.index(num)
        except:
            index = 0
        id = 1
        for num in range(index, index + 31):
            if len(str(id)) == 1:
                date.append('03.0' + str(id))
                id = id + 1
            else:
                date.append('03.' + str(id))
                id = id + 1
            province.append(i)
            province_city.append(ci)
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
        if province_city[0] == '朝阳区':
            dataframe = pd.DataFrame(
                {'date': date, 'province': province, 'city': province_city, 'confirm': confirm, 'dead': dead,
                 'heal': heal})
            dataframe.to_csv("各省疫情情况.csv", index=False, sep=',')
        else:
            dataframe = pd.DataFrame(
                {'date': date, 'province': province, 'city': province_city, 'confirm': confirm, 'dead': dead,
                 'heal': heal})
            dataframe.to_csv("各省疫情情况.csv", index=False, sep=',', header=False, mode='a')