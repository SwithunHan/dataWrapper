import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataWrapper.settings')
django.setup()


def main():
    from house import models
    models.Community.objects.create(**{
        'id': 1,
        'title': "贵园南里丁区",
        'link': "/admin",
        'district': "犯得上广泛士大夫",
        'bizcircle': "三个股东身份",
        'tagList': "的故事非官方",
        'onsale': 666,
        'onrent': 555,
        'year': 1005,
        'housetype': "两室一厅",
        'cost': "5-3",
        'service': "法国电视公司",
        'company': "的事告诉对方",
        'building_num': 55,
        'house_num': 1000,
        'price': 10,
        'city': "bj"
    })


if __name__ == '__main__':
    main()
    print("Done....")
