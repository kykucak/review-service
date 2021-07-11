from django.db.models import Count, Avg
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

import tldextract

from .models import Review, Shop
from .serializers import ReviewSerializer, ShopSerializer
from .filters import ShopsFilter, ReviewsFilter


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReviewsFilter
    ordering_fields = []
    ordering = ["-date_created"]

    def create(self, request, *args, **kwargs):
        """
        Changes "shop_link" in request.data to "shop_id" for correct creating a new review
        """
        request.data["shop"] = 1
        self.is_review_body_valid(self.get_serializer(data=request.data))  # checks if body data is valid

        shop_pk = self.get_shop_pk(request.data.pop("shop_link"))
        request.data["shop"] = shop_pk

        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Changes "shop_link" in request.data to "shop_id" for correct updating a review,
        if "shop_link" is in a request.data
        """
        self.is_review_body_valid(self.get_serializer(instance=self.get_object(), data=request.data, partial=True))

        if "shop_link" in request.data:
            shop_pk = self.get_shop_pk(request.data.pop("shop_link"))
            request.data["shop"] = shop_pk

        return super().partial_update(request, *args, **kwargs)

    @staticmethod
    def get_shop_pk(link: str):
        domain_name = tldextract.extract(link).domain
        shop, created = Shop.objects.get_or_create(name=domain_name.capitalize(), domain_name=domain_name)
        if created:
            shop.link = link
            shop.save()

        return shop.pk

    @staticmethod
    def is_review_body_valid(serializer: ReviewSerializer):
        serializer.is_valid(raise_exception=True)


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
