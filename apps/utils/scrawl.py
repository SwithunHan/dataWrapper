import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataWrapper.settings')
django.setup()

from utils import core
from house import models

from DataWrapper.settings import CITY
import pandas as pd


def get_communitylist(city):
    res = []
    for community in models.Community.objects.all():
        if community.city == city:
            res.append(community.title)
    return res


list1 = []


def open_csv():
    source_data = pd.read_csv('testcsv.csv')
    list = source_data.values.tolist()
    for i in range(0, len(list)):
        list1.append(list[i][1])
    return list1


if __name__ == "__main__":
    regionlist = open_csv()  # only pinyin support
    city = CITY
    # print(regionlist)
    # core.GetHouseByRegionlist(city, regionlist)
    # core.GetRentByRegionlist(city, regionlist)
    # Init,scrapy celllist and insert database; could run only 1st time
    # core.GetCommunityByRegionlist(city, regionlist)
    communitylist = get_communitylist(city)  # Read celllist from database
    core.GetHouseByCommunitylist(city, communitylist)
    core.GetSellByCommunitylist(city, communitylist)
    # core.GetRentByCommunitylist(city,communitylist)
