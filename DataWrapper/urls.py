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

from house.views import HouseViewSet, CommunityViewSet, DistributionViewSet, UserViewset, HousePriceAreaViewSet, \
    HouseTypeViewSet, HouseNumberViewSet, sellNumberAreaViewSet, HouseMaxPriceAreaViewSet, HouseTypeSellViewSet, \
    HouseMinPriceAreaViewSet, YearsAndsellPriceViewSet, DynamicViewSet, Web_sign_newViewSet, Web_sign_oldViewSet, \
    DecorationCountViewSet,DecorationPriceViewSet,FloorCountViewSet,DistrictUtilPriceViewSet

routers = DefaultRouter()
routers.register(r'api/houselist', HouseViewSet, base_name="houselist")
routers.register(r'api/community', CommunityViewSet, base_name="community")
routers.register(r'api/distribution', DistributionViewSet, base_name="distribution")
routers.register(r'api/registered', UserViewset, base_name="users")
routers.register(r'api/housepricearea', HousePriceAreaViewSet, base_name="housepricearea")
routers.register(r'api/housetype', HouseTypeViewSet, base_name="housetype")
routers.register(r'api/housenumber', HouseNumberViewSet, base_name="housenumber")

# 房屋类型成交量(完成)
routers.register(r'api/HouseTypeSell', HouseTypeSellViewSet, base_name='YHouseTypeSell')
# 每个行政区最高单价对比
routers.register(r'api/HouseMaxPriceArea', HouseMaxPriceAreaViewSet, base_name='HouseMaxPriceArea')
# 每个行政区最低单价对比
routers.register(r'api/HouseMinPriceArea', HouseMinPriceAreaViewSet, base_name='HouseMinPriceArea')


routers.register(r'api/YearsAndsellPrice', YearsAndsellPriceViewSet, base_name='YearsAndsellPriceViewSet')
# 动态新闻
routers.register(r'api/Dynamic', DynamicViewSet, base_name='Dynamic')
# 最新网签
routers.register(r'api/Web_sign_new', Web_sign_newViewSet, base_name='Web_sign_new')
# 网签数据
routers.register(r'api/Web_sign_old', Web_sign_oldViewSet, base_name='Web_sign_old')
# 装修情况和数量分析
routers.register(r'api/DecorationCount', DecorationCountViewSet, base_name='DecorationCount')
# 装修情况和价格分析
routers.register(r'api/DecorationPrice', DecorationPriceViewSet, base_name='DecorationPrice')
#楼层和其数量
routers.register(r'api/FloorCount', FloorCountViewSet, base_name='FloorCount')
# 各区域每平方米房价对比   每平方米房价取平均值  (连表查询)
routers.register(r'api/DistrictUtilPrice', DistrictUtilPriceViewSet, base_name='DistrictUtilPrice')

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
    url(r'^api/login/', obtain_jwt_token),
    url(r'^api/sellnumberarea/', sellNumberAreaViewSet)
]
