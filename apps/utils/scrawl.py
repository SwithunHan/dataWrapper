import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataWrapper.settings')
django.setup()

from utils import core
from house import models

from DataWrapper.settings import REGIONLIST, CITY


def get_communitylist(city):
    res = []
    for community in models.Community.objects.all():
        if community.city == city:
            res.append(community.title)
    return res


if __name__ == "__main__":
    regionlist = REGIONLIST  # only pinyin support
    city = CITY
    # core.GetHouseByRegionlist(city, regionlist)
    # core.GetRentByRegionlist(city, regionlist)
    # Init,scrapy celllist and insert database; could run only 1st time
    core.GetCommunityByRegionlist(city, regionlist)
    communitylist = get_communitylist(city)  # Read celllist from database
    core.GetHouseByCommunitylist(city, communitylist)
    core.GetSellByCommunitylist(city, communitylist)
    # core.GetRentByCommunitylist(city,communitylist)
