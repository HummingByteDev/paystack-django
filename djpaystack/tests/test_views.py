
import json
import pytest
from unittest.mock import patch, Mock
from django.test import TestCase, RequestFactory

from djpaystack.views import PaystackCallbackView


class TestPaystackCallbackView(TestCase):
    """Test PaystackCallbackView"""

    def setUp(self):
        self.factory = RequestFactory()
        self.view = PaystackCallbackView.as_view()

    def test_missing_reference_returns_400(self):
        """Test that missing reference returns 400"""
        request = self.factory.get('/callback/')
        response = self.view(request)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('Missing transaction reference', data['message'])

    def test_successful_verification(self):
        """Test successful transaction callback"""
        request = self.factory.get('/callback/?reference=test_ref')

        mock_client = Mock()
        mock_client.transactions.verify.return_value = {
            'data': {
                'status': 'success',
                'reference': 'test_ref',
                'amount': 50000,
            }
        }

        with patch('djpaystack.views.PaystackClient', return_value=mock_client):
            response = self.view(request)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEqual(data['status'], 'success')

    def test_failed_verification(self):
        """Test failed transaction callback"""
        request = self.factory.get('/callback/?reference=test_ref')

        mock_client = Mock()
        mock_client.transactions.verify.return_value = {
            'data': {
                'status': 'failed',
                'reference': 'test_ref',
            }
        }

        with patch('djpaystack.views.PaystackClient', return_value=mock_client):
            response = self.view(request)
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.content)
            self.assertEqual(data['status'], 'failed')

    def test_trxref_parameter(self):
        """Test that trxref parameter also works"""
        request = self.factory.get('/callback/?trxref=test_ref')

        mock_client = Mock()
        mock_client.transactions.verify.return_value = {
            'data': {
                'status': 'success',
                'reference': 'test_ref',
            }
        }

        with patch('djpaystack.views.PaystackClient', return_value=mock_client):
            response = self.view(request)
            self.assertEqual(response.status_code, 200)

    def test_paystack_error_handled(self):
        """Test that PaystackError during verification is handled"""
        from djpaystack.exceptions import PaystackAPIError

        request = self.factory.get('/callback/?reference=test_ref')

        mock_client = Mock()
        mock_client.transactions.verify.side_effect = PaystackAPIError(
            "Transaction not found", status_code=404
        )

        with patch('djpaystack.views.PaystackClient', return_value=mock_client):
            response = self.view(request)
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.content)
            self.assertIn('error', data['data'])
