import datetime
import json
import re

from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Max, Min
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, mixins, status, authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from .filters import HouseFilter, CommunityFilter, HousetypeFilter, HouseStateFilter
from .models import Houseinfo, Community
from .serializers import HouseinfoSerializer, CommunitySerializer, DistrictSerializer, UserRegSerializer, \
    HousePriceAreaSerializer, HouseTypeSerializer, HouseNumberSerializer

from rest_framework import filters

User = get_user_model()


class HousePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


# Create your views here.
# 小区列表
class CommunityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("=title",)
    filter_class = CommunityFilter
    pagination_class = HousePagination


# 房屋信息列表
class HouseViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Houseinfo.objects.extra(select={'key': 'houseID'}).all()
    serializer_class = HouseinfoSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = HouseFilter
    pagination_class = HousePagination


# 每个区小区数量
class DistributionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    queryset = Community.objects.values("district").annotate(value=Count("district"))
    serializer_class = DistrictSerializer


# 用户注册登陆
class UserViewset(CreateModelMixin, viewsets.GenericViewSet):
    '''
    用户
    '''
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    # 验证方式
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    # 注册时生成token
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["username"] = user.username

        headers = self.get_success_headers(serializer.data)

        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


# 每个区的平均房价（未完成）
class HousePriceAreaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Houseinfo.objects.all()
    serializer_class = HousePriceAreaSerializer
    pagination_class = HousePagination


# 行政区房屋成交量(未完成)
def get_years(string):
    return int(re.findall('(\d{4})', str(string))[0])


def sellNumberAreaViewSet(request):
    max_year = get_years(Houseinfo.objects.aggregate(Max('updatedate'))['updatedate__max'])
    min_year = get_years(Houseinfo.objects.aggregate(Min('updatedate'))['updatedate__min'])
    dict_list = []
    area_list = ['朝阳', '海淀', '东城', '西城', '丰台', '石景山', '通州', '昌平', '大兴', '亦庄开发区', '顺义', '房山', '门头沟', '平谷', '怀柔', '密云',
                 '延庆']
    for year in range(min_year, max_year + 1):
        print(year)
        dict1 = {'name': year}
        start_date = datetime.datetime(year, 1, 1, 0, 0, 0)
        end_date = datetime.datetime(year, 12, 31, 23, 59, 59)
        for area in area_list:
            house = Houseinfo.objects.filter(houseState='成交', updatedate__range=(start_date, end_date),
                                             community__district=area)
            for item in house:
                district = item.community.district
                item.community_id = district
            house = house.aggregate(Count("community"))['community__count']
            # if area != '亦庄开发区':
            #     area = area + "区"
            dict1[area] = house
        dict_list.append(dict1)

    return HttpResponse(json.dumps(dict_list))


# 查找各行政区内各种类型的房屋数量
class HouseTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Houseinfo.objects.filter().values("housetype").annotate(value=Count("housetype"))
    serializer_class = HouseTypeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = HousetypeFilter
    pagination_class = HousePagination


# 各个行政区内房屋数量
class HouseNumberViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Houseinfo.objects.filter().values("community__district").annotate(value=Count("community__district"))
    serializer_class = HouseNumberSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = HouseStateFilter
    pagination_class = HousePagination
