import datetime
import json
import re
from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Max, Min, Avg
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
from .models import Houseinfo, Community, Dynamic, Web_sign_new, Web_sign_old
from .serializers import HouseinfoSerializer, CommunitySerializer, DistrictSerializer, UserRegSerializer, \
    HousePriceAreaSerializer, HouseTypeSerializer, HouseNumberSerializer, HouseMaxPriceAreaSerializer, \
    HouseMinPriceAreaSerializer, YearsAndsellPriceSerializer, DynamicSerializer, Web_sign_newSerializer, \
    Web_sign_oldSerializer, DecorationCountSerializer, DecorationPriceSerializer, FloorCountSerializer, \
    DistrictUtilPriceSerializer

from rest_framework import filters

User = get_user_model()


class HousePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class InfoPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 5


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


# 每个行政区小区数量
class DistributionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    queryset = Community.objects.values("district").annotate(value=Count("district"))
    # print(queryset)
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


# 每个区的平均房价
class HousePriceAreaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    queryset = Community.objects.values('district').annotate(value=Avg("price"))
    serializer_class = HousePriceAreaSerializer
    pagination_class = HousePagination


# 行政区房屋成交量走势图
def get_years(string):
    return int(re.findall('(\d{4})', str(string))[0])


def sellNumberAreaViewSet(request):
    max_year = get_years(Houseinfo.objects.aggregate(Max('updatedate'))['updatedate__max'])
    min_year = get_years(Houseinfo.objects.aggregate(Min('updatedate'))['updatedate__min'])
    dict_list = []
    area_list = ['朝阳', '海淀', '东城', '西城', '丰台', '石景山', '通州', '昌平', '大兴', '亦庄开发区', '顺义', '房山', '门头沟', '平谷', '怀柔', '密云',
                 '延庆']
    for year in range(min_year, max_year + 1):
        # print(year)
        dict1 = {'name': year}
        start_date = datetime.datetime(year, 1, 1, 0, 0, 0)
        end_date = datetime.datetime(year, 12, 31, 23, 59, 59)
        for area in area_list:
            house = Houseinfo.objects.filter(houseState='成交').filter(updatedate__range=(start_date, end_date)).filter(
                community__district=area)
            for item in house:
                district = item.community.district
                item.community_id = district
            house = house.aggregate(Count("community"))['community__count']
            # if area != '亦庄开发区':
            #     area = area + "区"
            dict1[area] = house
        dict_list.append(dict1)
        a = json.dumps(dict_list)

    return HttpResponse(a)


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


# 不同户型成交量对比(饼状图或柱状图)（完成）
class HouseTypeSellViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Houseinfo.objects.filter(houseState='成交').values("housetype").annotate(value=Count("housetype"))
    serializer_class = HouseTypeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = HousetypeFilter


# 每个行政区最高单价对比
class HouseMaxPriceAreaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    queryset = Houseinfo.objects.filter(houseState='在售').values("community").annotate(value=Max('totalPrice'))
    serializer_class = HouseMinPriceAreaSerializer
    pagination_class = HousePagination


# 每个行政区最低单价对比
class HouseMinPriceAreaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    # queryset = Houseinfo.objects.values('totalPrice').annotate(value=Max("totalPrice")).values('community_id')

    queryset = Houseinfo.objects.filter(houseState='在售').values("community").annotate(value=Min('totalPrice'))
    serializer_class = HouseMaxPriceAreaSerializer
    pagination_class = HousePagination


# 建房时间和出售价格对比
class YearsAndsellPriceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    queryset = Houseinfo.objects.filter(houseState='在售').aggregate(Avg("totalPrice"))
    # print(queryset)
    serializer_class = YearsAndsellPriceSerializer
    pagination_class = HousePagination


# 动态新闻(完成)
class DynamicViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Dynamic.objects.all().order_by('-date_time')
    # print(queryset)
    serializer_class = DynamicSerializer
    pagination_class = InfoPagination


# 网签最新数据展示，完成
class Web_sign_newViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Web_sign_new.objects.all().order_by('-Date')
    serializer_class = Web_sign_newSerializer
    pagination_class = HousePagination


# 网签数据可视化，完成
class Web_sign_oldViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Web_sign_old.objects.all()
    serializer_class = Web_sign_oldSerializer
    pagination_class = HousePagination


# 装修情况和数量分析 完成
class DecorationCountViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Houseinfo.objects.values('decoration').annotate(value=Count('decoration'))
    serializer_class = DecorationCountSerializer
    pagination_class = HousePagination


# 装修情况和价格分析  完成
class DecorationPriceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Houseinfo.objects.filter(houseState='在售').values('decoration').annotate(value=Avg('totalPrice'))
    # print(queryset)
    serializer_class = DecorationPriceSerializer
    pagination_class = HousePagination


# 楼层和其数量 完成(数据出错)
class FloorCountViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Houseinfo.objects.values('floor').annotate(value=Count('floor'))
    serializer_class = FloorCountSerializer
    pagination_class = HousePagination


# 各区域每平方米房价对比   每平方米房价取平均值  (连表查询)
class DistrictUtilPriceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Houseinfo.objects.values('community__district').annotate(value=Avg('unitPrice'))
    serializer_class = DistrictUtilPriceSerializer
    pagination_class = HousePagination

# 二手房总价对比
# class DistrictUtilPriceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
#     queryset = Houseinfo.objects.values('community__district').annotate(value=Avg('unitPrice'))
#     serializer_class = DistrictUtilPriceSerializer
#     pagination_class = HousePagination
