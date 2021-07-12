from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from ..models import Shop, Review


class ShopListTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("shops")
        create_test_shops_and_reviews()

    def test_shop_list_when_no_query_params(self):
        """Checks if 2 shops were returned, when no query params were passed"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Checks ordering
        self.assertEqual(response.data[0].get("name"), "Rozetka")
        self.assertEqual(response.data[1].get("name"), "Foxtrot")

    def test_response_rozetka_when_name_is_rozetka(self):
        """Checks if serialized rozetka shop is returned, when name=rozetka"""
        data = {
            "name": "rozetka"
        }
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("name"), "Rozetka")
        self.assertEqual(response.data[0].get("link"), "https://rozetka.com.ua/")

    def test_empty_list_when_name_is_wrong(self):
        """Checks if no shops is returned, when name is wrong"""
        data = {
            "name": "somethingwrong"
        }
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_shops_order_when_order_is_asc_reviews(self):
        """Checks if ascending order by amount of reviews is used"""
        data = {
            "order": "reviews"
        }
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get("name"), "Rozetka")
        self.assertEqual(response.data[1].get("name"), "Foxtrot")

    def test_shops_order_when_order_is_desc_reviews(self):
        """Checks if descending order by amount of reviews is used"""
        data = {
            "order": "-reviews"
        }
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get("name"), "Foxtrot")
        self.assertEqual(response.data[1].get("name"), "Rozetka")

    def test_shops_order_when_order_is_asc_rate(self):
        """Checks if ascending order by average rate of reviews is used, when order=rate"""
        data = {
            "order": "rate"
        }
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get("name"), "Rozetka")
        self.assertEqual(response.data[1].get("name"), "Foxtrot")

    def test_shops_order_when_order_is_desc_rate(self):
        """Checks if descending order by average rate of reviews is used, when order=-rate"""
        data = {
            "order": "-rate"
        }
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get("name"), "Foxtrot")
        self.assertEqual(response.data[1].get("name"), "Rozetka")

    def test_shops_order_when_order_is_wrong(self):
        """Checks if standard shops order is used, when order='somethingworng'"""
        data = {
            "order": "somethingwrong"
        }
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get("name"), "Rozetka")
        self.assertEqual(response.data[1].get("name"), "Foxtrot")


class ReviewViewSetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_test_shops_and_reviews()

    # -------------------------------------LIST---------------------------

    def test_review_list_when_no_query_params(self):
        """
        Checks if review list is returned in right order(descending date_created) and has right length,
        when no query params are passed
        """
        url = reverse("review-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 8)

    def test_review_list_when_author_is_passed(self):
        """
        Checks if review list with author_email equals to passed author is returned,
        """
        url = reverse("review-list")
        data = {
            "author": "user3@email.com"
        }
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("author_email"), "user3@email.com")
        self.assertEqual(response.data[0].get("title"), "Review #3")

    def test_review_list_when_wrong_author_is_passed(self):
        """Checks if empty list is returned when wrong author is passed"""
        url = reverse("review-list")
        data = {
            "author": "someuser@email.com"
        }
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # ------------------------------------CREATE----------------------












def create_test_shops_and_reviews():
    # Creating shops
    shop_1 = Shop.objects.create(
        name="Rozetka",
        domain_name="rozetka",
        link="https://rozetka.com.ua/"
    )
    shop_2 = Shop.objects.create(
        name="Foxtrot",
        domain_name="foxtrot",
        link="https://www.foxtrot.com.ua/"
    )

    # Creating reviews
    for review_id in range(2, 10):
        shop = shop_1 if review_id < 5 else shop_2
        Review.objects.create(
            title=f"Review #{review_id}",
            content="Blalalallalla",
            shop=shop,
            stars=review_id // 2,
            author_email=f"user{review_id}@email.com"
        )