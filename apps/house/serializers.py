from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Houseinfo, Hisprice, Community, Rentinfo


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
    key = serializers.IntegerField()

    class Meta:
        model = Houseinfo
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    num = serializers.IntegerField()

    class Meta:
        model = Community
        fields = ("district", "num")


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
