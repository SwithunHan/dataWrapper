# -*- coding: utf-8 -*-
import os
import re
from datetime import datetime
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataWrapper.settings')
django.setup()

from bs4 import BeautifulSoup
from house import models
import time
import datetime
import urllib.request
import logging
from utils import misc
from .insert_sql import insertCommunity, insertHouseinfo, insertRentinfo, insertHisprice

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


# 根据行政区获取小区列表函数打印日志
def GetCommunityByRegionlist(city, regionlist):
    logging.info("Get Community Infomation")
    starttime = datetime.datetime.now()
    for regionname in regionlist:
        try:
            get_community_perregion(city, regionname)
            logging.info(regionname + "Done")
        except Exception as e:
            logging.error(e)
            logging.error(regionname + "Fail")
            pass
    endtime = datetime.datetime.now()
    logging.info("Run time: " + str(endtime - starttime))


# 获取小区列表
def get_community_perregion(city, regionname):
    baseUrl = u"http://%s.lianjia.com/" % (city)
    url = baseUrl + u"xiaoqu/" + 'rs' + regionname + "/"
    source_code = misc.get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')

    if check_block(soup):
        return
    total_pages = misc.get_total_pages(url)

    if total_pages == None:
        row = models.Community.select().count()
        raise RuntimeError("Finish at %s because total_pages is None" % row)

    for page in range(1, total_pages + 1):
        if page > 0:
            url_page = baseUrl + u"xiaoqu/" + "pg%d" % page + "rs" + regionname + '/'
            source_code = misc.get_source_code(url_page)
            soup = BeautifulSoup(source_code, 'lxml')

            nameList = soup.findAll("li", {"class": "clear"})
            i = 0
            log_progress("GetCommunityByRegionlist",
                         regionname, page, total_pages)
            data_source = []
            for name in nameList:  # Per house loop
                i = i + 1
                info_dict = {}
                try:
                    communitytitle = name.find("div", {"class": "title"})
                    title = communitytitle.get_text().strip('\n')
                    link = communitytitle.a.get('href')
                    info_dict.update({u'title': title})
                    info_dict.update({u'link': link})

                    district = name.find("a", {"class": "district"})
                    info_dict.update({u'district': district.get_text()})

                    bizcircle = name.find("a", {"class": "bizcircle"})
                    info_dict.update({u'bizcircle': bizcircle.get_text()})

                    tagList = name.find("div", {"class": "tagList"})
                    if tagList.get_text() == '\n':
                        info_dict.update({u'tagList': ''})
                        info_dict.update({u'subStation': ''})
                    else:
                        info_dict.update({u'tagList': re.findall('近地铁+(.*?线)([\u4e00-\u9fa5]+)',
                                                                 tagList.get_text().strip('\n'))[0][0]})

                        subStation = \
                            re.findall('近地铁+(.*?线)([\u4e00-\u9fa5]+)', tagList.get_text().strip('\n'))[0][
                                1]
                        info_dict.update({u'subStation': subStation})

                    # tagList = name.find("div", {"class": "tagList"})
                    # info_dict.update({u'tagList':tagList.get_text().strip('\n')})

                    onsale = name.find("a", {"class": "totalSellCount"})
                    info_dict.update(
                        {u'onsale': int(onsale.span.get_text().strip('\n'))})

                    web_sign = name.find("a", {"title": title + u"网签"})
                    info_dict.update(
                        {u'web_sign': int(re.findall('30天成交(\d+)套', web_sign.get_text().strip('\n'))[0])})

                    onrent = name.find("a", {"title": title + u"租房"})
                    info_dict.update(
                        {u'onrent': int(onrent.get_text().strip('\n').split(u'套')[0])})

                    info_dict.update({u'id': int(name.get('data-housecode'))})

                    price = name.find("div", {"class": "totalPrice"})
                    info_dict.update({u'price': int(price.span.get_text().strip('\n'))})

                    communityinfo, img_link = get_communityinfo_by_url(link)
                    # print(img_link)

                    info_dict.update({u'img_link': img_link})

                    for key, value in communityinfo.items():
                        if key == "year":
                            info_dict.update({key: int(re.findall('(\d+)', value)[0])})

                        elif key == 'building_num':
                            info_dict.update({key: int(re.findall('(\d+)', value)[0])})

                        elif key == 'house_num':
                            info_dict.update({key: int(re.findall('(\d+)', value)[0])})
                        else:
                            info_dict.update({key: value})

                    info_dict.update({u'city': city})
                    print(info_dict)
                    # print(len(info_dict))
                except:
                    continue
                # communityinfo insert into mysql
                data_source.append(info_dict)
        for data in data_source:
            try:
                insertCommunity(data)
            except:
                continue
        print(len(data_source))
        time.sleep(1)


# 获取小区详细信息列表
def get_communityinfo_by_url(url):
    source_code = misc.get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')

    if check_block(soup):
        return

    img = soup.find('div', {'class': 'imgThumbnailList'}).ol.li
    if img == None:
        img_link = 'https://s1.ljcdn.com/feroot/pc/asset/img/blank.gif?_v=20190409122206'
    else:
        img_link = re.sub('\d+x\d+.jpg', '710x400.jpg',
                          soup.find('div', {'class': 'imgThumbnailList'}).ol.li.img.get('src'))

    communityinfos = soup.findAll("div", {"class": "xiaoquInfoItem"})
    res = {}
    for info in communityinfos:
        key_type = {
            u"建筑年代": u'year',
            u"建筑类型": u'housetype',
            u"物业费用": u'cost',
            u"物业公司": u'service',
            u"开发商": u'company',
            u"楼栋总数": u'building_num',
            u"房屋总数": u'house_num',
        }
        try:
            key = info.find("span", {"xiaoquInfoLabel"})
            value = info.find("span", {"xiaoquInfoContent"})
            key_info = key_type[key.get_text().strip()]
            value_info = value.get_text().strip()
            res.update({key_info: value_info})

        except:
            continue
    return res, img_link


# 根据小区爬取在售房源信息
def GetHouseByCommunitylist(city, communitylist):
    logging.info("Get House Infomation")
    starttime = datetime.datetime.now()
    for community in communitylist:
        try:
            get_house_percommunity(city, community)
        except Exception as e:
            logging.error(e)
            logging.error(community + "Fail")
            pass
    endtime = datetime.datetime.now()
    logging.info("Run time: " + str(endtime - starttime))


def get_house_percommunity(city, communityname):
    baseUrl = u"http://%s.lianjia.com/" % (city)
    url = baseUrl + u"ershoufang/rs" + \
          urllib.request.quote(communityname.encode('utf8')) + "/"
    source_code = misc.get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')

    if check_block(soup):
        return
    total_pages = misc.get_total_pages(url)

    if total_pages == None:
        row = models.Houseinfo.select().count()
        raise RuntimeError("Finish at %s because total_pages is None" % row)

    for page in range(total_pages):
        if page > 0:
            url_page = baseUrl + \
                       u"ershoufang/pg%drs%s/" % (page,
                                                  urllib.request.quote(communityname.encode('utf8')))
            source_code = misc.get_source_code(url_page)
            soup = BeautifulSoup(source_code, 'lxml')

        nameList = soup.findAll("li", {"class": "clear"})
        i = 0
        log_progress("GetHouseByCommunitylist",
                     communityname, page + 1, total_pages)
        data_source = []
        hisprice_data_source = []
        for name in nameList:  # per house loop
            i = i + 1
            info_dict = {}
            try:
                housetitle = name.find("div", {"class": "title"})
                info_dict.update({u'title': housetitle.a.get_text().strip()})
                info_dict.update({u'link': housetitle.a.get('href')})

                houseaddr = name.find("div", {"class": "address"})
                if city == 'bj':
                    info = houseaddr.div.get_text().split('/')
                else:
                    info = houseaddr.div.get_text().split('|')
                info_dict.update({u'community': communityname})
                info_dict.update({u'housetype': info[1].strip()})
                info_dict.update({u'square': float(re.findall(r'(.*?)[\u4e00-\u9fa5]+', info[2].strip())[0])})
                info_dict.update({u'direction': info[3].strip()})
                info_dict.update({u'decoration': info[4].strip()})

                housefloor = name.find("div", {"class": "flood"})
                floor_all = housefloor.div.get_text().split(
                    '-')[0].strip().split(' ')
                info_dict.update({u'floor': re.findall(r'(.*?)/.*?/.*?', floor_all[0].strip())[0]})
                info_dict.update(
                    {u'years': int(re.findall(r'.*?/(\d+)[\u4e00-\u9fa5]+/.*?', floor_all[-1].strip())[0])})

                followInfo = name.find("div", {"class": "followInfo"})
                info_dict.update({u'followInfo': int(re.findall('(\d+)人关注', followInfo.get_text())[0])})

                tax = name.find("div", {"class": "tag"})
                info_dict.update({u'tag': tax.get_text().strip()})

                totalPrice = name.find("div", {"class": "totalPrice"})
                info_dict.update({u'totalPrice': float(totalPrice.span.get_text())}
                                 )
                unitPrice = name.find("div", {"class": "unitPrice"})
                info_dict.update({u'unitPrice': float(unitPrice.get('data-price'))})
                info_dict.update({u'houseID': int(unitPrice.get('data-hid'))})
                # print(info_dict)
            except:
                continue
            # houseinfo insert into mysql
            data_source.append(info_dict)
            hisprice_data_source.append(
                {"houseID": info_dict["houseID"], "totalPrice": info_dict["totalPrice"]})
            # print(hisprice_data_source)
        for data in data_source:
            try:
                insertHouseinfo(data)
            except:
                continue
            # print(data_source)

            # models.Houseinfo.insert(**info_dict).upsert().execute()

        for data in hisprice_data_source:
            try:
                insertHisprice(data)
            except:
                continue

        time.sleep(1)


# 根据小区爬成交房源信息
def GetSellByCommunitylist(city, communitylist):
    logging.info("Get Sell Infomation")
    starttime = datetime.datetime.now()
    for community in communitylist:
        try:
            get_sell_percommunity(city, community)
        except Exception as e:
            logging.error(e)
            logging.error(community + "Fail")
            pass
    endtime = datetime.datetime.now()
    logging.info("Run time: " + str(endtime - starttime))


def get_sell_percommunity(city, communityname):
    baseUrl = u"http://%s.lianjia.com/" % (city)
    url = baseUrl + u"chengjiao/rs" + \
          urllib.request.quote(communityname.encode('utf8')) + "/"
    source_code = misc.get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')

    if check_block(soup):
        return
    total_pages = misc.get_total_pages(url)

    if total_pages == None:
        row = models.Sellinfo.select().count()
        raise RuntimeError("Finish at %s because total_pages is None" % row)

    for page in range(total_pages):
        if page > 0:
            url_page = baseUrl + \
                       u"chengjiao/pg%drs%s/" % (page,
                                                 urllib.request.quote(communityname.encode('utf8')))
            source_code = misc.get_source_code(url_page)
            soup = BeautifulSoup(source_code, 'lxml')

        log_progress("GetSellByCommunitylist",
                     communityname, page + 1, total_pages)
        data_source = []
        for ultag in soup.findAll("ul", {"class": "listContent"}):
            for name in ultag.find_all('li'):
                info_dict = {}
                try:
                    housetitle = name.find("div", {"class": "title"})
                    if housetitle.get_text().strip().split()[1] == '车位':
                        continue
                    else:
                        info_dict.update({u'title': housetitle.get_text().strip()})
                        info_dict.update({u'link': housetitle.a.get('href')})
                        houseID = housetitle.a.get(
                            'href').split("/")[-1].split(".")[0]
                        if 'B' in list(houseID.strip()):
                            info_dict.update({u'houseID': int(re.findall('[A-Z](\d+)', houseID.strip())[0])})
                        else:
                            info_dict.update({u'houseID': int(houseID.strip())})

                        house = housetitle.get_text().strip().split(' ')
                        info_dict.update({u'community': communityname})
                        info_dict.update(
                            {u'housetype': house[1].strip() if 1 < len(house) else 0})
                        info_dict.update(
                            {u'square': float(re.findall('(.*?)[\u4e00-\u9fa5]+', house[2].strip())[0]) if 2 < len(
                                house) else 0})

                        houseinfo = name.find("div", {"class": "houseInfo"})
                        info = houseinfo.get_text().split('|')
                        info_dict.update({u'direction': info[0].strip()})
                        info_dict.update(
                            {u'decoration': info[1].strip() if 1 < len(info) else ''})

                        housefloor = name.find("div", {"class": "positionInfo"})
                        floor_all = housefloor.get_text().strip().split(' ')
                        info_dict.update({u'floor': floor_all[0].strip()})
                        info_dict.update(
                            {u'years': int(re.findall(r'(\d+)[\u4e00-\u9fa5]+', floor_all[-1].strip())[0])})

                        followInfo1 = name.find("div", {"class": "dealHouseInfo"})
                        # followInfo = followInfo1.find("span", {"class": "dealHouseTxt"})
                        if followInfo1 is None:
                            info_dict.update(
                                {u'tag': ''})
                        else:
                            followInfo = followInfo1.find("span", {"class": "dealHouseTxt"})
                            info_dict.update(
                                {u'tag': followInfo.span.get_text().strip()})

                        totalPrice = name.find("div", {"class": "totalPrice"})
                        # print(totalPrice.span.get_text.strip())
                        if totalPrice.span is None:
                            info_dict.update(
                                {u'totalPrice': 0})

                        else:
                            if len(list(re.findall('\d[*]+', totalPrice.span.get_text().strip()))) > 0:
                                url = info_dict['link']
                                source_code = misc.get_source_code(url)
                                soup1 = BeautifulSoup(source_code, 'lxml')
                                price = soup1.find('div', {'class': 'price'})
                                totalPrice_in = price.span.i.get_text().strip()
                                unitPrice_in = price.b.get_text().strip()

                                dealDate_in1 = soup1.findAll('div', {"class": "chengjiao_record"})[0]
                                dealDate_in2 = dealDate_in1.ul.li.p.get_text()
                                dealDate_in3 = re.findall('.*?,(\d+-\d+-\d+)[\u4e00-\u9fa5]', dealDate_in2)[0]

                                info_dict.update({u'totalPrice': float(totalPrice_in)})
                            else:
                                info_dict.update(
                                    {u'totalPrice': totalPrice.span.get_text().strip()})

                        unitPrice = name.find("div", {"class": "unitPrice"})
                        if unitPrice.span is None:
                            info_dict.update(
                                {u'unitPrice': 0})
                        else:
                            if unitPrice.span.get_text().strip() == '下载APP查看成交>':
                                info_dict.update({u'unitPrice': float(unitPrice_in)})
                            else:
                                info_dict.update(
                                    {u'unitPrice': float(unitPrice.span.get_text().strip())})

                        dealDate = name.find("div", {"class": "dealDate"})
                        if dealDate.get_text().strip() == '近30天内成交':
                            info_dict.update(
                                {u'updatedate': dealDate_in3})
                        else:
                            info_dict.update(
                                {u'updatedate': dealDate.get_text().strip().replace('.', '-')})
                        info_dict.update({u'houseState': u'成交'})
                        # print(info_dict)
                        # print(len(info_dict))
                        # print(type(info_dict['updateDate']))
                except:
                    continue
                # Sellinfo insert into mysql
                data_source.append(info_dict)
                # print(len(data_source))
                # model.Sellinfo.insert(**info_dict).upsert().execute()
        for data in data_source:
            try:
                insertHouseinfo(data)
            except:
                continue

        # with models.database.atomic():
        #     if data_source:
        #         models.Sellinfo.insert_many(data_source).upsert().execute()
        time.sleep(1)


# 根据小区爬租房信息
def GetRentByCommunitylist(city, communitylist):
    logging.info("Get Rent Infomation")
    starttime = datetime.datetime.now()
    for community in communitylist:
        try:
            get_rent_percommunity(city, community)
        except Exception as e:
            logging.error(e)
            logging.error(community + "Fail")
            pass
    endtime = datetime.datetime.now()
    logging.info("Run time: " + str(endtime - starttime))


def get_rent_percommunity(city, communityname):
    baseUrl = u"http://%s.lianjia.com/" % (city)
    url = baseUrl + u"zufang/rs" + \
          urllib.request.quote(communityname.encode('utf8')) + "/"
    source_code = misc.get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')

    if check_block(soup):
        return
    total_pages = misc.get_total_pages(url)

    if total_pages == None:
        row = models.Rentinfo.select().count()
        raise RuntimeError("Finish at %s because total_pages is None" % row)
    for page in range(total_pages):
        if page > 0:
            url_page = baseUrl + u"zufang/%s/pg%d/" % (communityname, page)
            source_code = misc.get_source_code(url_page)
            soup = BeautifulSoup(source_code, 'lxml')
        i = 0
        log_progress("GetRentByRegionlist", communityname, page + 1, total_pages)
        data_source = []
        for ultag in soup.findAll("div", {"class": 'content__list'}):
            for name in ultag.find_all('div', {"class": 'content__list--item'}):
                i = i + 1
                info_dict = {}
                try:
                    housetitle = name.div.p.a
                    info_dict.update({u'housetitle': housetitle.get_text().strip()})
                    # print(info_dict)
                    link = "https://bj.lianjia.com" + housetitle.get('href')
                    info_dict.update({u'link': "https://bj.lianjia.com" + housetitle.get('href')})
                    # print(info_dict)
                    houseID = int(re.findall('[A-Z]+(\d+)', housetitle.get('href').split('/')[-1].split('.')[0])[0])
                    info_dict.update({"houseID": houseID})
                    # print(info_dict)
                    regin = name.findAll('p', {"class": 'content__list--item--des'})[0]
                    community_name = regin.get_text().split('/')

                    # print(community_name)
                    meters = float(re.findall('(\d+)㎡', community_name[1].strip())[0])
                    # print(meters)
                    info_dict.update({"meters": meters})
                    direction = community_name[2]
                    info_dict.update({"direction": direction.strip()})
                    housetype = community_name[3].strip()
                    # print(housetype)
                    info_dict.update({"housetype": housetype})
                    price = name.div.find('span', {"class": "content__list--item-price"})
                    # print(price)
                    price = int(price.em.get_text())
                    info_dict.update({"price": price})
                    # print(price)
                    lable = name.div.find('p', {"class": "content__list--item--bottom oneline"})
                    # print(lable)
                    lable = ' '.join(lable.get_text().split())
                    info_dict.update({"lable": lable})
                    shelf_time, rent_time, floor, subway = get_information(link)
                    # print(shelf_time.strip().split()[2])
                    # print(lable)
                    info_dict.update({'shelf_time': shelf_time.strip().split()[2]})
                    info_dict.update({'rent_time': rent_time})
                    info_dict.update({'floor': floor})
                    info_dict.update({'subway': subway})
                    # 小区名称
                    info_dict.update({'region': communityname})
                    print(info_dict)

                except:
                    continue

            data_source.append(info_dict)
            # model.Rentinfo.insert(**info_dict).upsert().execute()
        for data in data_source:
            try:
                insertRentinfo(data)
            except:
                continue
        #
        # with models.database.atomic():
        #     if data_source:
        #         models.Rentinfo.insert_many(data_source).upsert().execute()
        # time.sleep(1)


def get_information(link):
    source_code = misc.get_source_code(link)
    soup = BeautifulSoup(source_code, 'lxml')

    if check_block(soup):
        return
    # res = requests.get(link, headers=headers)
    # soup = BeautifulSoup(res.content, 'lxml')
    shelf_time = soup.find('div', {"class": 'content__subtitle'})
    shelf_time = shelf_time.get_text()

    uls = soup.find('div', {"class", "content__article__info"})
    # 租期
    rent_time = uls.ul.findAll('li')[4].get_text()
    rent_time = re.findall('租期：(\d[\u4e00-\u9fa5]+)', rent_time)
    if len(rent_time) == 0:
        rent_time = 0
    else:
        rent_time = rent_time[0]
    # print(rent_time)
    # 楼层
    floor = uls.ul.findAll('li')[7].get_text()
    floor = re.findall('楼层：(.*)', floor)[0]
    # print(floor)
    # 地址交通
    info1 = soup.find('div', {"class": 'content--flat w1150'})
    info1 = info1.find('div', {'class': 'content__article__info4'})
    ul = info1.ul.li.findAll('span')
    li_len = info1.ul.findAll('li')
    # print(li_len)
    address_list = []
    for i in range(len(li_len)):
        # span =u'距离'+ li_len[i].span.get_text()+ul[i].get_text()
        span = li_len[i].findAll('span')
        address = u"距离" + span[0].get_text() + span[1].get_text()
        # print(address)
        address_list.append(address)
    # print(address_list)
    # print('|'.join(address_list))
    subway = '|'.join(address_list)
    return shelf_time, rent_time, floor, subway


# 根据行政区爬取房源信息
def GetHouseByRegionlist(city, regionlist=[u'xicheng']):
    starttime = datetime.datetime.now()
    for regionname in regionlist:
        logging.info("Get Onsale House Infomation in %s" % regionname)
        try:
            get_house_perregion(city, regionname)
        except Exception as e:
            logging.error(e)
            pass
    endtime = datetime.datetime.now()
    logging.info("Run time: " + str(endtime - starttime))


def get_house_perregion(city, district):
    baseUrl = u"http://%s.lianjia.com/" % (city)
    url = baseUrl + u"ershoufang/%s/" % district
    source_code = misc.get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')
    if check_block(soup):
        return
    total_pages = misc.get_total_pages(url)
    if total_pages == None:
        row = models.Houseinfo.select().count()
        raise RuntimeError("Finish at %s because total_pages is None" % row)

    for page in range(total_pages):
        if page > 0:
            url_page = baseUrl + u"ershoufang/%s/pg%d/" % (district, page)
            source_code = misc.get_source_code(url_page)
            soup = BeautifulSoup(source_code, 'lxml')
        i = 0
        log_progress("GetHouseByRegionlist", district, page + 1, total_pages)
        data_source = []
        hisprice_data_source = []
        for ultag in soup.findAll("ul", {"class": "sellListContent"}):
            for name in ultag.find_all('li'):
                i = i + 1
                info_dict = {}
                try:
                    housetitle = name.find("div", {"class": "title"})
                    info_dict.update(
                        {u'title': housetitle.a.get_text().strip()})
                    info_dict.update({u'link': housetitle.a.get('href')})
                    houseID = housetitle.a.get('data-housecode')
                    info_dict.update({u'houseID': houseID})

                    houseinfo = name.find("div", {"class": "houseInfo"})
                    if city == 'bj':
                        info = houseinfo.get_text().split('/')
                    else:
                        info = houseinfo.get_text().split('|')
                    info_dict.update({u'community': info[0]})
                    info_dict.update({u'housetype': info[1]})
                    info_dict.update({u'square': info[2]})
                    info_dict.update({u'direction': info[3]})
                    info_dict.update({u'decoration': info[4]})

                    housefloor = name.find("div", {"class": "positionInfo"})
                    info_dict.update({u'years': housefloor.get_text().strip()})
                    info_dict.update({u'floor': housefloor.get_text().strip()})

                    followInfo = name.find("div", {"class": "followInfo"})
                    info_dict.update(
                        {u'followInfo': followInfo.get_text().strip()})

                    taxfree = name.find("span", {"class": "taxfree"})
                    if taxfree == None:
                        info_dict.update({u"taxtype": ""})
                    else:
                        info_dict.update(
                            {u"taxtype": taxfree.get_text().strip()})

                    totalPrice = name.find("div", {"class": "totalPrice"})
                    info_dict.update(
                        {u'totalPrice': totalPrice.span.get_text()})

                    unitPrice = name.find("div", {"class": "unitPrice"})
                    info_dict.update(
                        {u'unitPrice': unitPrice.get("data-price")})
                except:
                    continue

                # Houseinfo insert into mysql
                data_source.append(info_dict)
                hisprice_data_source.append(
                    {"houseID": info_dict["houseID"], "totalPrice": info_dict["totalPrice"]})
                # model.Houseinfo.insert(**info_dict).upsert().execute()
                # model.Hisprice.insert(houseID=info_dict['houseID'], totalPrice=info_dict['totalPrice']).upsert().execute()

        with models.database.atomic():
            if data_source:
                models.Houseinfo.insert_many(data_source).upsert().execute()
            if hisprice_data_source:
                models.Hisprice.insert_many(
                    hisprice_data_source).upsert().execute()
        time.sleep(1)


# 根据行政区爬取租房信息
def GetRentByRegionlist(city, regionlist=[u'xicheng']):
    starttime = datetime.datetime.now()
    for regionname in regionlist:
        logging.info("Get Rent House Infomation in %s" % regionname)
        try:
            get_rent_perregion(city, regionname)
        except Exception as e:
            logging.error(e)
            pass
    endtime = datetime.datetime.now()
    logging.info("Run time: " + str(endtime - starttime))


def get_rent_perregion(city, district):
    baseUrl = u"http://%s.lianjia.com/" % (city)
    url = baseUrl + u"zufang/%s/" % district
    source_code = misc.get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')
    if check_block(soup):
        return
    total_pages = misc.get_total_pages(url)
    if total_pages == None:
        row = models.Rentinfo.select().count()
        raise RuntimeError("Finish at %s because total_pages is None" % row)

    for page in range(total_pages):
        if page > 0:
            url_page = baseUrl + u"zufang/%s/pg%d/" % (district, page)
            source_code = misc.get_source_code(url_page)
            soup = BeautifulSoup(source_code, 'lxml')
        i = 0
        log_progress("GetRentByRegionlist", district, page + 1, total_pages)
        data_source = []
        for ultag in soup.findAll("ul", {"class": "house-lst"}):
            for name in ultag.find_all('li'):
                i = i + 1
                info_dict = {}
                try:
                    housetitle = name.find("div", {"class": "info-panel"})
                    info_dict.update(
                        {u'title': housetitle.h2.a.get_text().strip()})
                    info_dict.update({u'link': housetitle.a.get("href")})
                    houseID = name.get("data-housecode")
                    info_dict.update({u'houseID': houseID})

                    region = name.find("span", {"class": "region"})
                    info_dict.update({u'region': region.get_text().strip()})

                    zone = name.find("span", {"class": "zone"})
                    info_dict.update({u'zone': zone.get_text().strip()})

                    meters = name.find("span", {"class": "meters"})
                    info_dict.update({u'meters': meters.get_text().strip()})

                    other = name.find("div", {"class": "con"})
                    info_dict.update({u'other': other.get_text().strip()})

                    subway = name.find("span", {"class": "fang-subway-ex"})
                    if subway == None:
                        info_dict.update({u'subway': ""})
                    else:
                        info_dict.update(
                            {u'subway': subway.span.get_text().strip()})

                    decoration = name.find("span", {"class": "decoration-ex"})
                    if decoration == None:
                        info_dict.update({u'decoration': ""})
                    else:
                        info_dict.update(
                            {u'decoration': decoration.span.get_text().strip()})

                    heating = name.find("span", {"class": "heating-ex"})
                    if decoration == None:
                        info_dict.update({u'heating': ""})
                    else:
                        info_dict.update(
                            {u'heating': heating.span.get_text().strip()})

                    price = name.find("div", {"class": "price"})
                    info_dict.update(
                        {u'price': int(price.span.get_text().strip())})

                    pricepre = name.find("div", {"class": "price-pre"})
                    info_dict.update(
                        {u'pricepre': pricepre.get_text().strip()})

                except:
                    continue
                # Rentinfo insert into mysql
                data_source.append(info_dict)
                # model.Rentinfo.insert(**info_dict).upsert().execute()

        with models.database.atomic():
            if data_source:
                models.Rentinfo.insert_many(data_source).upsert().execute()
        time.sleep(1)


# 检验ip是否禁
def check_block(soup):
    if soup.title.string == "414 Request-URI Too Large":
        logging.error(
            "Lianjia block your ip, please verify captcha manually at lianjia.com")
        return True
    return False


# 日志
def log_progress(function, address, page, total):
    logging.info("Progress: %s %s: current page %d total pages %d" %
                 (function, address, page, total))
