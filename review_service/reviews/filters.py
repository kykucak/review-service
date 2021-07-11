from django_filters import rest_framework as filters

from .models import Shop, Review


class ReviewsFilter(filters.FilterSet):
    author = filters.CharFilter(field_name="author_email", lookup_expr="exact")

    class Meta:
        model = Review
        fields = []


class ShopsFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="domain_name", lookup_expr="icontains")

    class Meta:
        model = Shop
        fields = []
