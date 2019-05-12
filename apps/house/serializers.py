from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Houseinfo, Hisprice, Community, Rentinfo, Dynamic, Web_sign_old, Web_sign_new


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = "__all__"


class HispriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hisprice
        fields = "__all__"


class RentinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rentinfo
        fields = "__all__"


class HouseinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Houseinfo
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField()
    name = serializers.CharField(source='district')

    class Meta:
        model = Community
        fields = ("name", "value")


class UserRegSerializer(serializers.ModelSerializer):
    '''
    用户注册
    '''

    # 验证用户名是否存在
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[
                                         UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    password = serializers.CharField(
        style={'input_type': 'password'}, label=True, write_only=True
    )

    # 密码加密保存新建用户
    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password')


class HousePriceAreaSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='district')
    value = serializers.FloatField()

    class Meta:
        model = Community
        fields = ("name", "value")


# 成交数量
class SellNumberAreaSerializer(serializers.ModelSerializer):
    # value = serializers.IntegerField()
    # name = serializers.CharField(source='community_district')
    #
    # class Meta:
    #     model = Houseinfo
    #     fields = ("name", "value")
    # community = CommunitySerializer()
    value = serializers.IntegerField()

    class Meta:
        model = Houseinfo
        fields = ("value",)


class HouseTypeSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField()
    name = serializers.CharField(source='housetype')

    class Meta:
        model = Houseinfo
        fields = ("name", "value")


class HouseNumberSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField()
    name = serializers.CharField(source='community__district')

    class Meta:
        model = Houseinfo
        fields = ("name", "value")


# 建房时间和出售价格对比
class YearsAndsellPriceSerializer(serializers.ModelSerializer):
    # name = serializers.IntegerField(source='years')
    # value = serializers.FloatField()

    class Meta:
        model = Houseinfo
        # fields = ("name", "value")
        fields = "__all__"


# 每个行政区最高单价对比
class HouseMaxPriceAreaSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='community')
    value = serializers.FloatField()

    class Meta:
        model = Houseinfo
        fields = ("name", "value")


# 每个行政区最高单价对比
class HouseMinPriceAreaSerializer(serializers.ModelSerializer):
    name = name = serializers.CharField(source='community')
    value = serializers.FloatField()

    class Meta:
        model = Houseinfo
        fields = ("name", "value")


# 动态新闻
class DynamicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dynamic
        fields = '__all__'


# 最新网签数据
class Web_sign_newSerializer(serializers.ModelSerializer):
    class Meta:
        model = Web_sign_new
        fields = '__all__'


# 网签数据
class Web_sign_oldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Web_sign_old
        fields = '__all__'


# 装修情况和数量分析
class DecorationCountSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='decoration')
    value = serializers.IntegerField()

    class Meta:
        model = Houseinfo
        fields = ("name", "value")


##装修情况和价格分析
class DecorationPriceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='decoration')
    value = serializers.IntegerField()

    class Meta:
        model = Houseinfo
        fields = ("name", "value")


# 楼层和其数量
class FloorCountSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='floor')
    value = serializers.IntegerField()

    class Meta:
        model = Houseinfo
        fields = ("name", "value")


# 各区域每平方米房价对比   每平方米房价取平均值  (连表查询)
class DistrictUtilPriceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='community__district')
    value = serializers.IntegerField()

    class Meta:
        model = Houseinfo
        # fields = ("name", "value")
        fields = '__all__'
        depth = 1


#北京各区域二手房总价对比

class DistrictUtilPriceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='community__district')
    value = serializers.IntegerField()

    class Meta:
        model = Houseinfo
        # fields = ("name", "value")
        fields = '__all__'
        depth = 1