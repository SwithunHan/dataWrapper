from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from .models import Houseinfo, Community
from .serializers import HouseinfoSerializer, CommunitySerializer, DistrictSerializer
from rest_framework import filters


# Create your views here.
class CommunityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("title",)


class HouseViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Houseinfo.objects.all()[:100]
    serializer_class = HouseinfoSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("community",)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print(request)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DistributionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Community.objects.values("district").annotate(num=Count("district"))
    # print(queryset)
    serializer_class = DistrictSerializer
