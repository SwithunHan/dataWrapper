from rest_framework import serializers
from .models import Office, OfficeSkills, OfficeType, OfficeArea, Company


class OfficeSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeSkills
        fields = "__all__"


class OOfficeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeType
        fields = "__all__"


class OfficeAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeArea
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    officeArea = OfficeAreaSerializer()

    class Meta:
        model = Company
        fields = "__all__"


class OfficeSerializer(serializers.ModelSerializer):
    officeType = OOfficeTypeSerializer()
    company = CompanySerializer()
    skills = OfficeSkillsSerializer(many=True)

    class Meta:
        model = Office
        fields = "__all__"
