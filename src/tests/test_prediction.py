from datetime import datetime
from unittest import mock

from django.urls import reverse

from rest_api import views
from tests import BaseTest


class TestPayment(BaseTest):

    @classmethod
    def setUpClass(cls):
        cls.url = reverse("restapi:price-estimation")
        cls.request_data = {
            'stock_name': 'AA',
            'date': '12-02-2015'
        }
        super().setUpClass()

    def test_success(self):
        response = self.client.get(self.url, data=self.request_data)
        self.assertEqual(response.status_code, 200)

    def test_fail(self):
        self.request_data.pop('stock_name')
        response = self.client.get(self.url, data=self.request_data)
        self.assertEqual(response.status_code, 400)