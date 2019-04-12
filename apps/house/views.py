from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, mixins, permissions, status, authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from .filters import HouseFilter, CommunityFilter
from .models import Houseinfo, Community
from .serializers import HouseinfoSerializer, CommunitySerializer, DistrictSerializer, UserRegSerializer

from rest_framework import filters

User = get_user_model()


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
    search_fields = ("=title",)
    filter_class = CommunityFilter
    pagination_class = HousePagination


class HouseViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Houseinfo.objects.extra(select={'key': 'houseID'}).all()
    serializer_class = HouseinfoSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = HouseFilter
    pagination_class = HousePagination


class DistributionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    queryset = Community.objects.values("district").annotate(num=Count("district"))
    serializer_class = DistrictSerializer


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
