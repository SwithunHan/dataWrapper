"""
网签数据
"""
import requests
import urllib3
from .insert_sql import insertWebsignOld

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_websignold():
    url = 'https://bj.ershoufangdata.com/api/volume/monthinfo?stime=2015-09-04&etime=2019-05-01'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
        'Referer': 'https://bj.ershoufangdata.com/volumn'
    }

    response = requests.get(url, headers=headers, verify=False)

    res = []
    json_list = response.json()
    for data in json_list['data']:
        time = data['Time']
        mounts = data['Total']

        a = dict({time: mounts})
        res.append(a)
    for data in res:
        try:
            insertWebsignOld(data)
        except:
            continue


"""
最近三日网签数据
需要每日定时爬取
"""


def get_zjsr():
    url = 'https://bj.ershoufangdata.com/api/volume/latest'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
        'Referer': 'https://bj.ershoufangdata.com/index'
    }

    data_source = []
    response = requests.get(url, headers=headers, verify=False)
    json_list = response.json()
    datas = json_list['data']
    for data in datas:
        Date = data['Date']
        House_num = data['House_num']
        House_square = data['House_square']
        Online_num = data['Online_num']
        Online_square = data['Online_square']

        a= dict({'Date':Date,'House_num':House_num,'House_square':House_square,'Online_num':Online_num,'Online_square':Online_square})
        data_source.append(a)
    for data in data_source:
        try:
            insertWebsignOld(data)
        except:
            continue

# get_zjsr()
# get_wangqian()