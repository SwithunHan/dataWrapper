from django_filters import rest_framework as filters
from .models import Community
from django.db.models import Q


class GoodsFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')

    @staticmethod
    def top_category_filter(queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Community
        fields = ['title']
