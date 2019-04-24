import os
import django

import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataWrapper.settings')
django.setup()

# dict = {'title': 'DBC加州小镇.南北通透三居室.户型方正.明厨明卫', 'link': 'https://bj.lianjia.com/ershoufang/101103476452.html',
#         'community': 'DBC加州小镇C区', 'housetype': '3室2厅', 'square': 130.99, 'direction': '南 北', 'decoration': '简装',
#         'floor': '中楼层(共15层)', 'years': 2010, 'followInfo': '69人关注/26次带看VR房源房本满五年随时看房629万单价48019元/平米',
#         'taxtype': 'VR房源房本满五年随时看房', 'totalPrice': 629.0, 'unitPrice': 48019.0, 'houseID': 101103476452}

dict1 = {'houseID': 101103742980, 'totalPrice': 565.0}

dict2 = {'title': 'BOBO自由城 2室2厅 109.3平米', 'link': 'https://bj.lianjia.com/chengjiao/101103897484.html',
         'houseID': 101103897484, 'community': 'BOBO自由城', 'housetype': '2室2厅', 'square': 109.3, 'direction': '南 北',
         'decoration': '精装', 'floor': '中楼层(共5层)', 'years': '2004年建板楼', 'taxtype': '房屋满五年', 'totalPrice': 600.0,
         'unitPrice': '54895', 'dealdate': '2019-03-08', 'houseState': '成交'}
1
dict3 = {'title': 'BOBO自由城 2室2厅 109.3平米', 'link': 'https://bj.lianjia.com/chengjiao/101103897484.html',
         'houseID': 101103897484, 'community': 'BOBO自由城', 'housetype': '2室2厅', 'square': 109.3, 'direction': '南 北',
         'decoration': '精装', 'floor': '中楼层(共5层)', 'years': '2004年建板楼', 'taxtype': '房屋满五年', 'totalPrice': 600.0,
         'unitPrice': '54895', 'dealdate': '2019-03-08', 'houseState': '成交'}

dict4 = {'title': '中海紫御公馆 2室2厅 89.98平米', 'link': 'https://bj.lianjia.com/chengjiao/101101689844.html',
         'houseID': 101101689844, 'community': '中海紫御公馆', 'housetype': '2室2厅', 'square': '89.98平米', 'direction': '南 北',
         'status': '精装', 'floor': '中楼层(共23层)', 'years': '2010年建板塔结合', 'source': '', 'totalPrice': '1030',
         'unitPrice': 114470.0, 'dealdate': '2017-10-09', 'houseState': '成交'}

dict = {'title': '定安里', 'link': 'https://bj.lianjia.com/xiaoqu/1111027376735/', 'district': '东城', 'bizcircle': '永定门',
        'tagList': '近地铁14号线东段景泰站', 'onsale': 12, 'onrent': 1, 'id': 1111027376735, 'price': 66547, 'year': 1963,
        'housetype': '板楼/平房', 'cost': '暂无信息', 'service': '无物业管理服务', 'company': '无开发商', 'building_num': 28,
        'house_num': 1801, 'city': 'bj'}

# a = datetime.datetime.strptime('2017-01-05','%Y-%m-%d 00:00:00.000000')


dict4 = {'title': 'NAGA上院 3室2厅 305平米', 'link': 'https://bj.lianjia.com/chengjiao/101089756045.html',
         'houseID': 101089756045, 'community': '万国城MOMA', 'housetype': '3室2厅', 'square': 305.0, 'direction': '东 南',
         'decoration': '精装', 'floor': '低楼层(共12层)', 'years': 2008, 'tag': '近地铁', 'totalPrice': '2200',
         'unitPrice': 72132.0, 'updatedate': '2017-01-05', 'houseState': '成交'}
# dict5 = {'title': '新景家园东区', 'link': 'https://bj.lianjia.com/xiaoqu/1111027380930/', 'district': '东城',
#          'bizcircle': '崇文门', 'tagList': '近地铁5号线磁器口站', 'onsale': 35, 'onrent': 10, 'id': 1111027380930, 'price': 101811,
#          'year': 2002, 'housetype': '板楼/塔板结合', 'cost': '1.14至2.48元/平米/月', 'service': '北京新世界物业管理有限公司',
#          'company': '北京崇文新世界房地产发展有限公司', 'building_num': 15, 'house_num': 5389, 'city': 'bj'}

dict5 = {'title': '万国城MOMA 3室2厅 3000万', 'link': 'https://bj.lianjia.com/ershoufang/101103597424.html',
         'community': '万国城MOMA', 'housetype': '3室2厅', 'square': 281.95, 'direction': '东 南 北', 'decoration': '精装',
         'floor': '底层(共26层)', 'years': 2006, 'followInfo': '33人关注/0次带看VR房源房本满两年3000万单价106402元/平米',
         'tag': 'VR房源房本满两年', 'totalPrice': 3000.0, 'unitPrice': 106402.0, 'houseID': 1011073597424}
dict6 = {'houseID': 101103597424, 'totalPrice': 3000.0}

dict7 = {'title': '国瑞城中区', 'link': 'https://bj.lianjia.com/xiaoqu/1111027374691/', 'district': '东城', 'bizcircle': '崇文门',
         'tagList': '近地铁5号线', 'subStation': '崇文门站', 'onsale': 29, 'onrent': 12, 'id': 1111027374691, 'price': 95670,
         'year': 2004, 'housetype': '板楼/塔板结合', 'cost': '1.1至3.1元/平米/月', 'service': '北京国瑞物业管理有限公司',
         'company': '北京国瑞兴业地产有限公司', 'building_num': 14, 'house_num': 3402, 'city': 'bj'}
dict8 = {'title': '首城汇景湾', 'link': 'https://bj.lianjia.com/xiaoqu/1111063599263/', 'district': '平谷',
         'bizcircle': '平谷其它', 'tagList': '', 'subStation': '', 'onsale': 37, 'web_sign': 1, 'onrent': 1,
         'id': 1111063599263, 'price': 23758,
         'img_link': 'https://image1.ljcdn.com/hdic-resblock/fc85e15e-0e59-4c44-9fc8-3a71cafac33f.jpg.710x400.jpg', 'year': 2014,
         'housetype': '板楼', 'cost': '2.46至3.46元/平米/月', 'service': '北京城承物业管理有限责任公司', 'company': '北京首城置业有限公司',
         'building_num': 34, 'house_num': 2651, 'city': 'bj'}


def main(dict):
    from house import models
    # community = models.Community.objects.get(title=dict['community'])
    # print(dict['community'])
    # dict['community'] = community
    # models.Houseinfo.objects.create(**dict)
    # print(1)
    # models.Community.objects.create(**dict)
    # print(2)
    # models.Hisprice.objects.create(**dict)
    models.Community.objects.create(**dict)


main(dict8)
import datetime as time


def test_time():
    from django.utils import timezone as datetime
    # print(type(time.datetime.now()))
    # from datetime import datetime  # 导入datetime模块
    # stamp = datetime(2017, 10, 7)  # 生成一个datetime对象
    # stamp.strftime('%Y-%m-%d')  # 转换  #结果显示：'2017-10-07 00:00:00'
    # print(stamp)
    # print(type(stamp))
    value = '2017-10-7'
    date = datetime.datetime.strptime(value, '%Y-%m-%d')
    print(date)
    print(type(date))


# main(dict7)
# print(a)
# test_time()
print("Done....")
