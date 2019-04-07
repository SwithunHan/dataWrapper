import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataWrapper.settings')
django.setup()

dict = {'title': 'DBC加州小镇.南北通透三居室.户型方正.明厨明卫', 'link': 'https://bj.lianjia.com/ershoufang/101103476452.html',
        'community': 'DBC加州小镇C区', 'housetype': '3室2厅', 'square': 130.99, 'direction': '南 北', 'decoration': '简装',
        'floor': '中楼层(共15层)', 'years': 2010, 'followInfo': '69人关注/26次带看VR房源房本满五年随时看房629万单价48019元/平米',
        'taxtype': 'VR房源房本满五年随时看房', 'totalPrice': 629.0, 'unitPrice': 48019.0, 'houseID': 101103476452}

dict1 = {'houseID': 101103742980, 'totalPrice': 565.0}

def main(dict):
    from house import models
    community = models.Community.objects.get(title=dict['community'])
    print(dict['community'])
    dict['community'] = community
    models.Houseinfo.objects.create(**dict)


main(dict)
print("Done....")
