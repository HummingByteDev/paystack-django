
import pytest
from unittest.mock import Mock, patch
from djpaystack import PaystackClient


class TestTransactionAPI:
    """Test Transaction API"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        with patch('djpaystack.settings.paystack_settings') as mock_settings:
            mock_settings.SECRET_KEY = 'sk_test_xxxxx'
            mock_settings.BASE_URL = 'https://api.paystack.co'
            mock_settings.TIMEOUT = 30
            mock_settings.MAX_RETRIES = 3
            mock_settings.VERIFY_SSL = True
            return PaystackClient()

    def test_initialize_transaction_success(self, client, mock_paystack_response):
        """Test successful transaction initialization"""
        mock_paystack_response['data'] = {
            'authorization_url': 'https://checkout.paystack.com/xxxxx',
            'access_code': 'xxxxx',
            'reference': 'test_ref_123'
        }

        with patch.object(client.session, 'request') as mock_request:
            mock_response = Mock()
            mock_response.json.return_value = mock_paystack_response
            mock_response.status_code = 200
            mock_request.return_value = mock_response

            response = client.transactions.initialize(
                email='test@example.com',
                amount=50000,
                reference='test_ref_123'
            )

            assert response['status'] is True
            assert 'authorization_url' in response['data']
            assert response['data']['reference'] == 'test_ref_123'

            # Verify request was made with correct parameters
            args, kwargs = mock_request.call_args
            assert kwargs['json']['email'] == 'test@example.com'
            assert kwargs['json']['amount'] == 50000

    def test_verify_transaction_success(self, client, mock_paystack_response):
        """Test successful transaction verification"""
        mock_paystack_response['data'] = {
            'reference': 'test_ref_123',
            'amount': 50000,
            'status': 'success',
            'customer': {'email': 'test@example.com'}
        }

        with patch.object(client.session, 'request') as mock_request:
            mock_response = Mock()
            mock_response.json.return_value = mock_paystack_response
            mock_response.status_code = 200
            mock_request.return_value = mock_response

            response = client.transactions.verify('test_ref_123')

            assert response['status'] is True
            assert response['data']['status'] == 'success'

    def test_list_transactions(self, client, mock_paystack_response):
        """Test listing transactions"""
        mock_paystack_response['data'] = [
            {'reference': 'ref1', 'amount': 50000},
            {'reference': 'ref2', 'amount': 30000}
        ]
        mock_paystack_response['meta'] = {
            'total': 2,
            'pageCount': 1
        }

        with patch.object(client.session, 'request') as mock_request:
            mock_response = Mock()
            mock_response.json.return_value = mock_paystack_response
            mock_response.status_code = 200
            mock_request.return_value = mock_response

            response = client.transactions.list(per_page=50, page=1)

            assert response['status'] is True
            assert len(response['data']) == 2

    def test_charge_authorization(self, client, mock_paystack_response):
        """Test charging with authorization code"""
        mock_paystack_response['data'] = {
            'reference': 'charge_ref_123',
            'amount': 50000,
            'status': 'success'
        }

        with patch.object(client.session, 'request') as mock_request:
            mock_response = Mock()
            mock_response.json.return_value = mock_paystack_response
            mock_response.status_code = 200
            mock_request.return_value = mock_response

            response = client.transactions.charge_authorization(
                authorization_code='AUTH_xxxxx',
                email='test@example.com',
                amount=50000
            )

            assert response['status'] is True
            assert response['data']['status'] == 'success'
