
import pytest
from unittest.mock import Mock, patch, MagicMock
from djpaystack import PaystackClient
from djpaystack.exceptions import (
    PaystackAPIError,
    PaystackAuthenticationError,
    PaystackNetworkError,
)


class TestPaystackClient:
    """Test PaystackClient class"""

    def test_client_initialization(self):
        """Test client initialization"""
        with patch('djpaystack.client.paystack_settings') as mock_settings:
            mock_settings.SECRET_KEY = 'sk_test_xxxxx'
            mock_settings.BASE_URL = 'https://api.paystack.co'
            mock_settings.TIMEOUT = 30
            mock_settings.MAX_RETRIES = 3
            mock_settings.VERIFY_SSL = True

            client = PaystackClient()
            assert client.secret_key == 'sk_test_xxxxx'
            assert client.base_url == 'https://api.paystack.co'
            assert client.timeout == 30

    def test_client_initialization_without_secret_key(self):
        """Test client initialization fails without secret key"""
        with patch('djpaystack.client.paystack_settings') as mock_settings:
            mock_settings.SECRET_KEY = None

            with pytest.raises(PaystackAuthenticationError):
                PaystackClient()

    def test_client_custom_secret_key(self):
        """Test client with custom secret key"""
        with patch('djpaystack.client.paystack_settings') as mock_settings:
            mock_settings.SECRET_KEY = 'sk_test_default'
            mock_settings.BASE_URL = 'https://api.paystack.co'
            mock_settings.TIMEOUT = 30

            client = PaystackClient(secret_key='sk_test_custom')
            assert client.secret_key == 'sk_test_custom'

    def test_get_headers(self):
        """Test request headers"""
        with patch('djpaystack.client.paystack_settings') as mock_settings:
            mock_settings.SECRET_KEY = 'sk_test_xxxxx'
            mock_settings.BASE_URL = 'https://api.paystack.co'
            mock_settings.TIMEOUT = 30

            client = PaystackClient()
            headers = client._get_headers()

            assert 'Authorization' in headers
            assert headers['Authorization'] == 'Bearer sk_test_xxxxx'
            assert headers['Content-Type'] == 'application/json'

    def test_successful_request(self, mock_paystack_response):
        """Test successful API request"""
        with patch('djpaystack.client.paystack_settings') as mock_settings:
            mock_settings.SECRET_KEY = 'sk_test_xxxxx'
            mock_settings.BASE_URL = 'https://api.paystack.co'
            mock_settings.TIMEOUT = 30
            mock_settings.LOG_REQUESTS = False
            mock_settings.LOG_RESPONSES = False
            mock_settings.VERIFY_SSL = True

            client = PaystackClient()

            with patch.object(client.session, 'request') as mock_request:
                mock_response = Mock()
                mock_response.json.return_value = mock_paystack_response
                mock_response.status_code = 200
                mock_request.return_value = mock_response

                response = client.get('transaction')

                assert response['status'] is True
                assert 'data' in response

    def test_failed_request(self):
        """Test failed API request"""
        with patch('djpaystack.client.paystack_settings') as mock_settings:
            mock_settings.SECRET_KEY = 'sk_test_xxxxx'
            mock_settings.BASE_URL = 'https://api.paystack.co'
            mock_settings.TIMEOUT = 30
            mock_settings.LOG_REQUESTS = False
            mock_settings.LOG_RESPONSES = False
            mock_settings.VERIFY_SSL = True

            client = PaystackClient()

            with patch.object(client.session, 'request') as mock_request:
                mock_response = Mock()
                mock_response.json.return_value = {
                    'status': False,
                    'message': 'Invalid parameters'
                }
                mock_response.status_code = 400
                mock_request.return_value = mock_response

                with pytest.raises(PaystackAPIError) as exc_info:
                    client.get('transaction')

                assert 'Invalid parameters' in str(exc_info.value)

    def test_network_error(self):
        """Test network error handling"""
        import requests

        with patch('djpaystack.client.paystack_settings') as mock_settings:
            mock_settings.SECRET_KEY = 'sk_test_xxxxx'
            mock_settings.BASE_URL = 'https://api.paystack.co'
            mock_settings.TIMEOUT = 30
            mock_settings.VERIFY_SSL = True

            client = PaystackClient()

            with patch.object(client.session, 'request') as mock_request:
                mock_request.side_effect = requests.exceptions.ConnectionError(
                    'Connection failed')

                with pytest.raises(PaystackNetworkError):
                    client.get('transaction')
