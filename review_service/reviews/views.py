from django.db.models import Count, Avg
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .models import Review, Shop
from .serializers import ReviewSerializer, ShopSerializer
from .filters import ShopsFilter


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ShopList(generics.ListAPIView):
    model = Shop
    serializer_class = ShopSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShopsFilter

    def get_queryset(self):
        order = self.request.query_params.get("order", " ")
        way = "-" if order[0] == "-" else ""
        if order == "reviews" or order == "-reviews":
            ordered_shops = Shop.objects.annotate(num_reviews=Count("reviews")).order_by(f"{way}num_reviews")
        elif order == "rate" or order == "-order":
            ordered_shops = Shop.objects.annotate(avg_rate=Avg("reviews__stars")).order_by(f"{way}avg_rate")
        else:
            ordered_shops = Shop.objects.all()

        return ordered_shops


@api_view(http_method_names=["GET"])
def get_shops(request, *args, **kwargs):
    """api/shops/?order=rate|reviews"""
    order = request.GET.get("order", " ")
    way = "-" if order[0] == "-" else ""
    if order == "reviews" or order == "-reviews":
        ordered_shops = Shop.objects.annotate(num_reviews=Count("reviews")).order_by(f"{way}num_reviews")
    elif order == "rate" or order == "-order":
        ordered_shops = Shop.objects.annotate(avg_rate=Avg("reviews__stars")).order_by(f"{way}avg_rate")
    else:
        ordered_shops = Shop.objects.all()
    shops_serializer = ShopSerializer(ordered_shops, many=True)

    return Response(shops_serializer.data)
