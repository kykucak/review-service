from django.test import TestCase

from ..models import Review, Shop


class ShopModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Shop.objects.create(
            name="Rozetka",
            domain_name="rozetka",
            link="https://rozetka.com.ua/"
        )

    def test_domain_name_label(self):
        shop = Shop.objects.get(name="Rozetka")
        field_label = shop._meta.get_field("domain_name").verbose_name
        self.assertEqual(field_label, "domain name")

    def test_name_max_length(self):
        shop = Shop.objects.get(name="Rozetka")
        max_length = shop._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_domain_name_max_length(self):
        shop = Shop.objects.get(name="Rozetka")
        max_length = shop._meta.get_field("domain_name").max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_name(self):
        shop = Shop.objects.get(name="Rozetka")
        expected_object_name = shop.name
        self.assertEqual(str(shop), expected_object_name)


class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        shop = Shop.objects.create(
            name="Rozetka",
            domain_name="rozetka",
            link="https://rozetka.com.ua/"
        )
        Review.objects.create(
            title="Test review",
            content="Test content lalalalal",
            shop=shop,
            stars=3,
            author_email="user@email.com",
        )

    def test_title_label(self):
        review = Review.objects.get(pk=1)
        field_label = review._meta.get_field("title").verbose_name
        self.assertEqual(field_label, "title")

    def test_title_max_length(self):
        review = Review.objects.get(pk=1)
        max_length = review._meta.get_field("title").max_length
        self.assertEqual(max_length, 155)

    def test_object_name_is_title_for_shop_name(self):
        review = Review.objects.get(pk=1)
        expected_object_name = f"{review.title} for {review.shop.name}"
        self.assertEqual(str(review), expected_object_name)
