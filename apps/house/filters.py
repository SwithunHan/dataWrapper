from django_filters import rest_framework as filters
from .models import Houseinfo, Community
from django.db.models import Q


class HouseFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = Houseinfo
        fields = ['community']


class CommunityFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = Community
        fields = ['title']


class SellFilter(filters.FilterSet):
    datamin = filters.DateFilter(field_name="updatedate", lookup_expr='gte')
    datamax = filters.DateFilter(field_name="updatedate", lookup_expr='lte')

    class Meta:
        model = Houseinfo
        fields = ['updatedate']


class HousetypeFilter(filters.FilterSet):
    community__district = filters.CharFilter(field_name="community__district")

    class Meta:
        model = Houseinfo
        fields = ['community__district']
