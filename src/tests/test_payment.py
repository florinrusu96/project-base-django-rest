from datetime import datetime
from unittest import mock

from django.urls import reverse

from rest_api import views
from tests import BaseTest


class TestPayment(BaseTest):

    @classmethod
    def setUpClass(cls):
        cls.url = reverse("restapi:payment")
        cls.request_data = {
            'credit_card_number': '1234567890123',
            'card_holder': "John Snow",
            'expiration_date': f"{datetime.today().year + 4}-02-02",
            'security_code': '123',
            'amount': 15
        }
        super().setUpClass()

    def test_cheap_payment_success(self):
        response = self.client.post(self.url, self.request_data)
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'card_holder': "John Snow",
            'expiration_date': f"{datetime.today().year + 4}-02-02",
            'amount': 15
        }
        self.assertEqual(response.data, expected_data)

    def test_expensive_payment_success(self):
        self.request_data['amount'] = 50
        response = self.client.post(self.url, self.request_data)
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'card_holder': "John Snow",
            'expiration_date': f"{datetime.today().year + 4}-02-02",
            'amount': 50
        }
        self.assertEqual(response.data, expected_data)

    def test_premium_payment_success(self):
        self.request_data['amount'] = 505
        response = self.client.post(self.url, self.request_data)
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'card_holder': "John Snow",
            'expiration_date': f"{datetime.today().year + 4}-02-02",
            'amount': 505
        }
        self.assertEqual(response.data, expected_data)

    def test_invalid_card_number(self):
        self.request_data['credit_card_number'] = 15125
        response = self.client.post(self.url, self.request_data)
        self.assertEqual(response.status_code, 400)

    def test_fail_expensive_payment(self):
        self.request_data['amount'] = 50
        with mock.patch('rest_api.external_service.ExpensivePaymentGateway', side_effect=Exception('Unavailable')):
            with mock.patch.object(views.PaymentCreate, "_process_cheap_payment") as _process_cheap_payment:
                self.client.post(self.url, self.request_data)
                _process_cheap_payment.assert_called_once()

    def test_fail_premium_payment_check_retry(self):
        self.request_data['amount'] = 505
        with self.assertRaises(Exception):
            with mock.patch('rest_api.external_service.PremiumPaymentGateway', side_effect=Exception('Unavailable')):
                with mock.patch.object(views.PaymentCreate, "_process_premium_payment",
                                       side_effect=views.PaymentCreate._process_premium_payment) as _premium_payment:
                    self.client.post(self.url, self.request_data)
                    self.assertEqual(_premium_payment.call_count, 3)

    def test_fail_premium_payment(self):
        self.request_data['amount'] = 505
        with self.assertRaises(Exception):
            with mock.patch('rest_api.external_service.PremiumPaymentGateway', side_effect=Exception('Unavailable')):
                self.client.post(self.url, self.request_data)
