import os
import django
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataWrapper.settings')
django.setup()


def insertCommunity(dicts):
    from house import models

    models.Community.objects.create(**dicts)


def insertHouseinfo(dicts):
    from house import models
    try:
        community = models.Community.objects.get(title=dicts['community'])
    # print(dicts['community'])
        dicts['community'] = community
    except:
        pass
    models.Houseinfo.objects.create(**dicts)


def insertRentinfo(dicts):
    from house import models
    models.Rentinfo.objects.create(**dicts)


# def insertSellinfo(dicts):
#     from house import models
#     models.Sellinfo.objects.create(**dicts)


def insertHisprice(dicts):
    from house import models
    models.Hisprice.objects.create(**dicts)
