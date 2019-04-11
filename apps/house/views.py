from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from .models import Houseinfo, Community
from .serializers import HouseinfoSerializer, CommunitySerializer, DistrictSerializer
from rest_framework import filters


class HousePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


# Create your views here.
class CommunityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("title",)
    pagination_class = HousePagination


class HouseViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Houseinfo.objects.extra(select={'key': 'houseID'}).all()
    serializer_class = HouseinfoSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('community',)
    pagination_class = HousePagination


class DistributionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Community.objects.values("district").annotate(num=Count("district"))
    # print(queryset)
    serializer_class = DistrictSerializer
