from django.db import models

from .fields import IntegerRangeField


class Shop(models.Model):
    name = models.CharField(max_length=100)
    domain_name = models.CharField(max_length=100)
    link = models.URLField()

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.CharField(max_length=155)
    content = models.TextField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="reviews")
    stars = IntegerRangeField(min_value=1, max_value=5)
    author_email = models.EmailField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} for {self.shop.name}"
