from django.shortcuts import render
from rest_framework import viewsets, mixins


# Create your views here.
class HouseViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass

