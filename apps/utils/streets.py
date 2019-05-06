import requests
import re
from lxml import etree
import random
import time
import pandas as pd
from utils.misc import hds

"""
抓取小区的街道信息
"""

Community = [u'dongcheng', u'xicheng', u'chaoyang', u'haidian', u'fengtai', u'shijingshan', u'changping', u'daxing',
              u'yizhuangkaifaqu', u'shunyi', u'fangshan'
    , u'mentougou', u'pinggu', u'huairou', u'tongzhou', u'miyun', u'yanqing']
Comms = []
def get_community():
    for c in Community:

        url = 'https://bj.lianjia.com/xiaoqu/'+c+'/'
        headers = {
            'Cookie': 'lianjia_uuid=7f039b3a-bbf2-d9de-d8b9-5336005d51f4; _smt_uid=5c9753a1.51acc9e4; UM_distinctid=169af1eb17212d-00ddff4358166c-1333062-144000-169af1eb1731cc; _ga=GA1.2.1263343797.1553421220; CNZZDATA1273627291=316933974-1554122674-https%253A%252F%252Fbj.lianjia.com%252F%7C1554528580; _jzqx=1.1553421218.1555485442.30.jzqsr=google%2Ecom|jzqct=/.jzqsr=google%2Ecom|jzqct=/; lianjia_ssid=451515cb-6112-4957-aaff-6990e8744091; select_city=110000; all-lj=3d8def84426f51ac8062bdea518a8717; TY_SESSION_ID=7bfee85e-bc22-41db-bbf3-e687254371b3; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1555298622,1555299754,1555485442,1555897184; CNZZDATA1253477573=1582917191-1553421069-https%253A%252F%252Fwww.google.com%252F%7C1555896510; _qzjc=1; CNZZDATA1254525948=392900369-1553420588-https%253A%252F%252Fwww.google.com%252F%7C1555895932; CNZZDATA1255633284=513532660-1553420679-https%253A%252F%252Fwww.google.com%252F%7C1555896987; CNZZDATA1255604082=1992926165-1553418717-https%253A%252F%252Fwww.google.com%252F%7C1555896047; _jzqa=1.3930434968578725000.1553421218.1555485442.1555897184.49; _jzqc=1; _jzqckmp=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22169c35cc48b6c7-08a0198b42622b-1333062-1327104-169c35cc48c6c1%22%2C%22%24device_id%22%3A%22169c35cc48b6c7-08a0198b42622b-1333062-1327104-169c35cc48c6c1%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _gid=GA1.2.1858219932.1555897188; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1555899685; _qzja=1.385584236.1553421218580.1555485442629.1555897183821.1555899671063.1555899685977.0.0.0.339.45; _qzjb=1.1555897183821.12.0.0.0; _qzjto=12.1.0; _jzqb=1.12.10.1555897184.1; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1',
            'User-Agent': hds[random.randint(0, len(hds) - 1)]['User-Agent'],
        }

        response = requests.get(url, headers=headers)
        tree = etree.HTML(response.text)
        # titles = tree.xpath("//div[@class='info']/div[@class='title']/a/text()")
        communitys = tree.xpath("//div[@data-role='ershoufang']/div[2]/a/text()")

        # print(len(communitys))
        for community in communitys:
            # print(community)
            Comms.append(community)

        time.sleep(random.randint(2,4))
    return Comms

C = get_community()
A = list(set(C))
name = ['街道']
test = pd.DataFrame(columns=name,data=A)
test.to_csv('testcsv.csv',encoding='utf-8')