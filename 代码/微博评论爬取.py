# -*- coding: utf-8 -*-
import requests, random, re
import time
import os
import csv
import sys
import json
import importlib
importlib.reload(sys)
from fake_useragent import UserAgent
from lxml import etree
import pandas as pd
import http.cookiejar as cookielib
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

cookies = cookielib.LWPCookieJar("Cookie.txt")
cookies.load(ignore_discard=True, ignore_expires=True)
# 将cookie转换成字典
cookie_dict = requests.utils.dict_from_cookiejar(cookies)
comments_ID = []
title_user_ids=[]
commentss=[]
dates=[]
article_urls=[]
title_user_NicNames=[]
title_user_genders=[]
reposts_counts=[]
comments_counts=[]
attitudes_counts=[]
def get_title_id():
    '''爬取战疫情首页的每个主题的ID'''
    for page in range(1,31):  # 每个页面大约有18个话题
        headers = {
            "User-Agent":
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",

        }
        time.sleep(1)
        # 该链接通过抓包获得
        api_url = 'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_600059_-_ctg1_600059&page=' + str(page)
        rep = requests.get(url=api_url, headers=headers,cookies=cookie_dict)
        for json in rep.json()['data']['statuses']:
            comment_ID = json['id']
            comments_ID.append(comment_ID)



def spider_title(comment_ID):
    try:
        article_url = 'https://m.weibo.cn/detail/' + comment_ID
        article_urls.append(article_url)
        html_text = requests.get(url=article_url, headers=headers,cookies=cookie_dict).text
        # 楼主ID
        title_user_id = re.findall('.*?"id": (.*?),.*?', html_text)[1]
        title_user_ids.append(title_user_id)
        # 楼主昵称
        title_user_NicName = re.findall('.*?"screen_name": "(.*?)",.*?', html_text)[0]
        title_user_NicNames.append(title_user_NicName)
        # 楼主性别
        title_user_gender = re.findall('.*?"gender": "(.*?)",.*?', html_text)[0]
        title_user_genders.append(title_user_gender)
        # 转发量
        reposts_count = re.findall('.*?"reposts_count": (.*?),.*?', html_text)[0]
        reposts_counts.append(reposts_count)
        # 评论量
        comments_count = re.findall('.*?"comments_count": (.*?),.*?', html_text)[0]
        comments_counts.append(comments_count)
        # 点赞量
        attitudes_count = re.findall('.*?"attitudes_count": (.*?),.*?', html_text)[0]
        attitudes_counts.append(attitudes_count)
    except:
        pass


def get_page(comment_ID, max_id, id_type):
    params = {
        'max_id': max_id,
        'max_id_type': id_type
    }
    url = ' https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id'.format(comment_ID, comment_ID)
    try:
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        pass


def parse_page(jsondata):
    if jsondata:
        items = jsondata.get('data')
        item_max_id = {}
        item_max_id['max_id'] = items['max_id']
        item_max_id['max_id_type'] = items['max_id_type']
        return item_max_id


def write_csv(jsondata):
    comments=''
    for json in jsondata['data']['data']:
        comments_text = json['text']
        comment_text = re.sub('<(S*?)[^>]*>.*?|<.*? />', '', comments_text)  # 正则匹配掉html标签
        comments+=comment_text
    return comments

def main():
    count_title = len(comments_ID)
    for count, comment_ID in enumerate(comments_ID):
        print("正在爬取第%s个话题，一共找到个%s话题需要爬取" % (count + 1, count_title))
        num=int(count/18)+1
        date='6月'+str(num)+'日'
        dates.append(date)
        spider_title(comment_ID)
        m_id = 0
        id_type = 0

        try:
            for page in range(1, 2):  # 用评论数量控制循环
                jsondata = get_page(comment_ID, m_id, id_type)
                comments=write_csv(jsondata)
                results = parse_page(jsondata)
                m_id = results['max_id']
                id_type = results['max_id_type']
                commentss.append(comments)
        except:
            pass




if __name__ == '__main__':
    get_title_id()
    main()
    if len(commentss)<len(dates):
        article_urls = article_urls[:len(commentss)]
        dates = dates[:len(commentss)]
        title_user_ids = title_user_ids[:len(commentss)]
        title_user_NicNames = title_user_NicNames[:len(commentss)]
        title_user_genders = title_user_genders[:len(commentss)]
        reposts_counts = reposts_counts[:len(commentss)]
        comments_counts = comments_counts[:len(commentss)]
        attitudes_counts = attitudes_counts[:len(commentss)]

    else:
        commentss=commentss[:len(dates)]

    dataframe = pd.DataFrame(
        {'article_url': article_urls, 'date': dates, 'title_user_id': title_user_ids, 'title_user_NicName': title_user_NicNames, 'title_user_gender': title_user_genders,
         'reposts_count': reposts_counts,'comments_count': comments_counts,'attitudes_count': attitudes_counts,'comments': commentss})
    dataframe.to_csv("微博评论数据.csv", index=False, sep=',')
