"""DataWrapper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

from house.views import HouseViewSet, CommunityViewSet, DistributionViewSet, UserViewset

routers = DefaultRouter()
routers.register(r'api/houselist', HouseViewSet, base_name="houselist")
routers.register(r'api/community', CommunityViewSet, base_name="community")
routers.register(r'api/distribution', DistributionViewSet, base_name="distribution")
routers.register(r'api/registered', UserViewset, base_name="users")
urlpatterns = [
    # xadmin url
    url(r'^admin/', admin.site.urls),
    # 图片路径
    url(r'^', include(routers.urls)),
    # 项目文档
    url(r'^docs/', include_docs_urls(title="项目文档")),
    # api登录
    url(r'^api-auth/', include('rest_framework.urls')),
    # 登陆
    url(r'^api/login/', obtain_jwt_token)
]
