
from unittest.mock import Mock, patch, MagicMock
import pytest
from djpaystack.client import PaystackClient


class TestCustomerAPI:
    """Test Customer API"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        with patch('djpaystack.client.paystack_settings') as mock_settings:
            mock_settings.SECRET_KEY = 'sk_test_xxxxx'
            mock_settings.BASE_URL = 'https://api.paystack.co'
            mock_settings.TIMEOUT = 30
            return PaystackClient()

    def test_create_customer(self, client, mock_paystack_response):
        """Test customer creation"""
        mock_paystack_response['data'] = {
            'email': 'test@example.com',
            'customer_code': 'CUS_xxxxx',
            'first_name': 'John',
            'last_name': 'Doe'
        }

        with patch.object(client.session, 'request') as mock_request:
            mock_response = Mock()
            mock_response.json.return_value = mock_paystack_response
            mock_response.status_code = 200
            mock_request.return_value = mock_response

            response = client.customers.create(
                email='test@example.com',
                first_name='John',
                last_name='Doe'
            )

            assert response['status'] is True
            assert response['data']['customer_code'] == 'CUS_xxxxx'

    def test_fetch_customer(self, client, mock_paystack_response):
        """Test fetching customer"""
        mock_paystack_response['data'] = {
            'email': 'test@example.com',
            'customer_code': 'CUS_xxxxx'
        }

        with patch.object(client.session, 'request') as mock_request:
            mock_response = Mock()
            mock_response.json.return_value = mock_paystack_response
            mock_response.status_code = 200
            mock_request.return_value = mock_response

            response = client.customers.fetch('test@example.com')

            assert response['status'] is True
            assert response['data']['email'] == 'test@example.com'
