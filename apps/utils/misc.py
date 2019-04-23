import requests
import random
from datetime import datetime
from bs4 import BeautifulSoup
import threading
from six.moves import urllib
import socket

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
    'Cookie': 'lianjia_uuid=7f039b3a-bbf2-d9de-d8b9-5336005d51f4; _smt_uid=5c9753a1.51acc9e4; UM_distinctid=169af1eb17212d-00ddff4358166c-1333062-144000-169af1eb1731cc; _ga=GA1.2.1263343797.1553421220; CNZZDATA1273627291=316933974-1554122674-https%253A%252F%252Fbj.lianjia.com%252F%7C1554528580; _jzqx=1.1553421218.1555485442.30.jzqsr=google%2Ecom|jzqct=/.jzqsr=google%2Ecom|jzqct=/; lianjia_ssid=451515cb-6112-4957-aaff-6990e8744091; select_city=110000; all-lj=3d8def84426f51ac8062bdea518a8717; TY_SESSION_ID=7bfee85e-bc22-41db-bbf3-e687254371b3; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1555298622,1555299754,1555485442,1555897184; CNZZDATA1253477573=1582917191-1553421069-https%253A%252F%252Fwww.google.com%252F%7C1555896510; _qzjc=1; CNZZDATA1254525948=392900369-1553420588-https%253A%252F%252Fwww.google.com%252F%7C1555895932; CNZZDATA1255633284=513532660-1553420679-https%253A%252F%252Fwww.google.com%252F%7C1555896987; CNZZDATA1255604082=1992926165-1553418717-https%253A%252F%252Fwww.google.com%252F%7C1555896047; _jzqa=1.3930434968578725000.1553421218.1555485442.1555897184.49; _jzqc=1; _jzqckmp=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22169c35cc48b6c7-08a0198b42622b-1333062-1327104-169c35cc48c6c1%22%2C%22%24device_id%22%3A%22169c35cc48b6c7-08a0198b42622b-1333062-1327104-169c35cc48c6c1%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _gid=GA1.2.1858219932.1555897188; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1555899685; _qzja=1.385584236.1553421218580.1555485442629.1555897183821.1555899671063.1555899685977.0.0.0.339.45; _qzjb=1.1555897183821.12.0.0.0; _qzjto=12.1.0; _jzqb=1.12.10.1555897184.1; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1',
    'User-Agent': hds[random.randint(0, len(hds) - 1)]['User-Agent'],

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


# ===========proxy ip spider, we do not use now because it is not stable===
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
