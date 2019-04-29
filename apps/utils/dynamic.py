"""
获取凤凰网，今日头条关于北京二手房的动态信息
"""

import requests
import time
from lxml import etree
from .insert_sql import insertDynamic

def get_jrtt():
    baseurl = 'https://www.toutiao.com/api/search/content/?'
    timestamp = time.time()
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    # print(dt)
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    dt_new = time.mktime(timeArray)
    timestamp = int(dt_new)
    # print(int(dt_new))
    # print(type(dt_new))
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': '0',
        'format': 'json',
        'keyword': '北京二手房',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': timestamp,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
        'Referer': 'https://www.toutiao.com/search/?keyword=%E5%8C%97%E4%BA%AC%E4%BA%8C%E6%89%8B%E6%88%BF',
        # ':authority': 'www.toutiao.com',
        'x-requested-with': 'XMLHttpRequest',
        'Cookie': 'UM_distinctid=16a6133f10641-019268cd075668-f353163-144000-16a6133f107850; csrftoken=771dbbc256c856b6683ecf0c26c4b58c; s_v_web_id=5182f377e5702bf4b0b5bfd6528a4cab; WEATHER_CITY=%E5%8C%97%E4%BA%AC; ccid=ee76a09519d8ed4ca42e556b84d75728; login_flag=163ca74ad06ff8cc77c47364bd7b0036; sessionid=1816623506979d3271f7f9b6fe459210; uid_tt=6d8dfc99aaad49e10cbac9ea534983f7; sid_tt=1816623506979d3271f7f9b6fe459210; sid_guard="1816623506979d3271f7f9b6fe459210|1556415643|15552000|Fri\054 25-Oct-2019 01:40:43 GMT"; tt_webid=75485971111; uuid="w:3929d00ab0a04217aa1fc580f16f2925"; tt_webid=75485971111; cp=5CC500A6ADD17E1; __tasessionId=rbyr2qnxt1556430254191; CNZZDATA1259612802=192005346-1556403589-%7C1556430589',
        # ':path': '/c/user/article/?page_type=1&user_id=63314328657&max_behot_time=0&count=20&as=A1652C3C8523F44&cp=5CC5A31F04445E1&_signature=ZhWy0BAQOtRvWcjFNb1PlmYVss',

    }

    response = requests.get(baseurl, params=params, headers=headers)
    res_json = response.json()
    # print(res_json)
    data = res_json.get('data')
    data_source = []
    for i in range(0, 7):
        info_dict = {}
        if data[i].get('ala_src') is None:

            title = data[i].get('title')
            info_dict.update(({'title':title}))
            link = str(data[i].get('source_url'))
            url = "https://www.toutiao.com" + link
            info_dict.update({'url':url})
            date_time = data[i].get('datetime')
            info_dict.update({'date_time':date_time})
            source = data[i].get('emphasized').get('source')
            info_dict.update({'source':source})

        else:
            continue
        data_source.append(info_dict)
    for data in data_source:
        try:
            insertDynamic(data)
        except:
            continue


def get_fh():
    s = requests.Session()

    url = 'https://ihouse.ifeng.com/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
        'Referer': 'https://ihouse.ifeng.com/'
    }

    response = s.get(url, headers=headers)

    # print(response.status_code)
    tree = etree.HTML(response.text)

    links = tree.xpath("//dd[@id='scrollToTopbox']/div/a/@href")
    # print(links)
    data_source = []
    for url in links:
        info_dict = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
            'Referer': 'https://ihouse.ifeng.com/',
        }
        response1 = s.get(url, headers=headers)
        # print(response.text.encode('utf-8'))
        response1.encoding = 'utf-8'
        tree = etree.HTML(response1.text)
        try:
            title = tree.xpath("/html/body/artical/div[2]/h1/text()")[0]
            info_dict.update(({'title': title}))
            info_dict.update({'url': url})
            date_time = tree.xpath("//artical/div[@class='w90 artical']/div/div[2]/text()")[0]
            info_dict.update({'date_time': date_time})
            source = '凤凰网房产'
            info_dict.update({'source': source})
        except:
            continue

        data_source.append(info_dict)
    for data in data_source:
        try:
            insertDynamic(data)
        except:
            continue
