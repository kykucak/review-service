from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import ReviewViewSet, ShopList

router = SimpleRouter()
router.register(r"reviews", ReviewViewSet, 'review')

urlpatterns = [
    path("", include(router.urls)),
    path("shops/", ShopList.as_view(), name="shops")
]
