from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from .models import Houseinfo, Community
from .serializers import HouseinfoSerializer, CommunitySerializer
from rest_framework import filters


# Create your views here.
class CommunityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("title",)


class HouseViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Houseinfo.objects.all()
    serializer_class = HouseinfoSerializer
