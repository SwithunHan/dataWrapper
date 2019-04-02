from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import Office, Company
from .serializers import OfficeSerializer, CompanySerializer
from django.db.models import Count
from rest_framework.response import Response


class OfficeListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer


class CompanyOfAreaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Company.objects.values("officeArea").annotate(Count('officeArea'))
    serializer_class = CompanySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(self.get_queryset())
