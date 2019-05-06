import requests
import random
from datetime import datetime
from bs4 import BeautifulSoup
import threading
from six.moves import urllib
import socket
"""
链家反爬应对，Cookie,随机User-Agent,代理池，线程
"""

hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
       {
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
       {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
       {
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},
       {
           'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
       {
           'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},
       {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
       {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
       {
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
       {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
       {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]


headers = {
    'User-Agent': hds[random.randint(0, len(hds) - 1)]['User-Agent'],
    'Cookie': 'lianjia_uuid=76342eac-9750-4c55-b2f8-1ca8fb6d4d3f; UM_distinctid=16a58586c189e9-0b28e75b5173d2-f353163-144000-16a58586c1984c; _smt_uid=5cc2a602.39f9c034; _ga=GA1.2.133286249.1556260356; all-lj=8e5e63e6fe0f3d027511a4242126e9cc; _qzjc=1; _jzqc=1; introduce=1; TY_SESSION_ID=61503be6-95be-452c-8bdc-eef3f6e31653; _jzqx=1.1556260351.1556413882.1.jzqsr=google%2Ecom|jzqct=/.-; ljref=pc_sem_baidu_ppzq_x; select_city=110000; lianjia_ssid=044c86d2-1b1b-4011-93dc-5e40cce66088; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1556355720,1556408318,1556413882,1556502087; CNZZDATA1253477573=71419478-1556255681-https%253A%252F%252Fwww.google.com%252F%7C1556498913; _jzqa=1.3570621167241082400.1556260351.1556413882.1556502087.5; _jzqy=1.1556502087.1556502087.1.jzqsr=baidu|jzqct=lianjia%20.-; _jzqckmp=1; CNZZDATA1255633284=1806359853-1556258324-https%253A%252F%252Fwww.google.com%252F%7C1556498902; CNZZDATA1255604082=2104261200-1556256991-https%253A%252F%252Fwww.google.com%252F%7C1556497184; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216a58586ea069a-0efb8dd6668cb9-f353163-1327104-16a58586ea1664%22%2C%22%24device_id%22%3A%2216a58586ea069a-0efb8dd6668cb9-f353163-1327104-16a58586ea1664%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fsp0.baidu.com%2F9q9JcDHa2gU2pMbgoY3K%2Fadrc.php%3Ft%3D06KL00c00fZg9KY0XQK60nVfAsKDN_uT000002k7c7C00000LY6lgt.THd_py78ph-90A3qmh7GuZR0T1Y4Pjm1n1w9PW0snj0drAFW0ZRqwbRLPj6YrDuAPbNDfWTvP1RdfbD3rjPjPjD4fWR%22%2C%22%24latest_referrer_host%22%3A%22sp0.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22lianjia%20%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22sousuo%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; _gid=GA1.2.1299327922.1556502092; lianjia_token=2.00192d61c26754bb34088048f34e100ab2; CNZZDATA1254525948=580960433-1556257502-https%253A%252F%252Fwww.google.com%252F%7C1556502186; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1556502221; _qzja=1.1719303520.1556260351182.1556413882373.1556502087217.1556502209052.1556502221693.0.0.0.18.5; _qzjb=1.1556502087217.4.0.0.0; _qzjto=4.1.0; _jzqb=1.4.10.1556502087.1',

}


def get_source_code(url):
    try:
        result = requests.get(
            url, headers=headers)
        # result = requests.get(url)
        source_code = result.content
    except Exception as e:
        print(e)
        return

    return source_code


def get_total_pages(url):
    source_code = get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')
    total_pages = 0
    try:
        page_info = soup.find('div', {'class': 'page-box house-lst-page-box'})
    except AttributeError as e:
        page_info = None

    # if it doesnot get total page, then return default value 50
    if page_info == None:
        return 1
    # '{"totalPage":5,"curPage":1}'
    page_info_str = page_info.get('page-data').split(',')[0]
    total_pages = int(page_info_str.split(':')[1])
    return total_pages

proxys_src = []
proxys = []


def spider_proxyip():
    try:
        for i in range(1, 4):
            url = 'http://www.xicidaili.com/nt/' + str(i)
            req = requests.get(
                url, headers=hds[random.randint(0, len(hds) - 1)])
            source_code = req.content
            soup = BeautifulSoup(source_code, 'lxml')
            ips = soup.findAll('tr')

            for x in range(1, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                proxy_host = "http://" + \
                             tds[1].contents[0] + ":" + tds[2].contents[0]
                proxy_temp = {"http": proxy_host}
                proxys_src.append(proxy_temp)
    except Exception as e:
        print("spider_proxyip exception:")
        print(e)


def test_proxyip_thread(i):
    socket.setdefaulttimeout(5)
    url = "http://bj.lianjia.com"
    try:
        proxy_support = urllib.request.ProxyHandler(proxys_src[i])
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        res = urllib.request.Request(
            url, headers=hds[random.randint(0, len(hds) - 1)])
        source_cod = urllib.request.urlopen(res, timeout=10).read()
        if source_cod.find(b'\xe6\x82\xa8\xe6\x89\x80\xe5\x9c\xa8\xe7\x9a\x84IP') == -1:
            proxys.append(proxys_src[i])
    except Exception as e:
        return
    # print(e)


def test_proxyip():
    print("proxys before:" + str(len(proxys_src)))
    threads = []
    try:
        for i in range(len(proxys_src)):
            thread = threading.Thread(target=test_proxyip_thread, args=[i])
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
    except Exception as e:
        print(e)
    print("proxys after:" + str(len(proxys)))


def prepare_proxy():
    spider_proxyip()
    test_proxyip()


def readurl_by_proxy(url):
    try:
        tet = proxys[random.randint(0, len(proxys) - 1)]
        proxy_support = urllib.request.ProxyHandler(tet)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        req = urllib.request.Request(
            url, headers=hds[random.randint(0, len(hds) - 1)])
        source_code = urllib.request.urlopen(req, timeout=10).read()
        if source_code.find(b'\xe6\x82\xa8\xe6\x89\x80\xe5\x9c\xa8\xe7\x9a\x84IP') != -1:
            proxys.remove(tet)
            print('proxys remove by IP traffic, new length is:' + str(len(proxys)))
            return None

    except Exception as e:
        proxys.remove(tet)
        print('proxys remove by exception:')
        print(e)
        print('proxys new length is:' + str(len(proxys)))
        return None

    return source_code
