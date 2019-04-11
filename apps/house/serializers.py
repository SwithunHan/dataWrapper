from rest_framework import serializers

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
