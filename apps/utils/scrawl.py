import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataWrapper.settings')
django.setup()

from utils import core
from house import models

from DataWrapper.settings import CITY
import pandas as pd
import threading
from utils import web_sign

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
    # core.GetCommunityByRegionlist(city, regionlist)
    communitylist = get_communitylist(city)  # Read celllist from database
    # # core.GetHouseByCommunitylist(city,communitylist)
    # core.GetSellByCommunitylist(city,communitylist)
    # core.GetRentByCommunitylist(city,communitylist)
    t1 = threading.Thread(target=core.GetHouseByCommunitylist, args=(city, communitylist))
    t2 = threading.Thread(target=core.GetSellByCommunitylist, args=(city, communitylist))
    t3 = threading.Thread(target=core.GetRentByCommunitylist,args=(city, communitylist))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    print('结束')
    # web_sign.get_websignold()
    # core.GetRentByCommunitylist(city,communitylist)
