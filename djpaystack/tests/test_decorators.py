
import pytest
from unittest.mock import patch
from django.http import JsonResponse

from djpaystack.decorators import handle_paystack_errors
from djpaystack.exceptions import PaystackError, PaystackAPIError


class TestHandlePaystackErrors:
    """Test handle_paystack_errors decorator"""

    def test_successful_function(self):
        """Test decorator passes through successful responses"""
        @handle_paystack_errors
        def my_view():
            return JsonResponse({'status': 'success'})

        response = my_view()
        assert response.status_code == 200

    def test_paystack_error_returns_400(self):
        """Test PaystackError is caught and returns 400"""
        @handle_paystack_errors
        def my_view():
            raise PaystackError("Payment failed")

        response = my_view()
        assert response.status_code == 400

    def test_paystack_api_error_returns_400(self):
        """Test PaystackAPIError is caught and returns 400"""
        @handle_paystack_errors
        def my_view():
            raise PaystackAPIError("Invalid request", status_code=422)

        response = my_view()
        assert response.status_code == 400

    def test_unexpected_error_returns_500(self):
        """Test unexpected exceptions return 500 with generic message"""
        @handle_paystack_errors
        def my_view():
            raise ValueError("Something unexpected")

        response = my_view()
        assert response.status_code == 500

    def test_unexpected_error_hides_details(self):
        """Test that unexpected error details are not leaked"""
        @handle_paystack_errors
        def my_view():
            raise RuntimeError("sensitive db info")

        response = my_view()
        import json
        data = json.loads(response.content)
        assert 'sensitive' not in data['message']
        assert data['message'] == 'An unexpected error occurred'

    def test_paystack_error_message_included(self):
        """Test that PaystackError message is included in response"""
        @handle_paystack_errors
        def my_view():
            raise PaystackError("Insufficient funds")

        response = my_view()
        import json
        data = json.loads(response.content)
        assert data['message'] == 'Insufficient funds'

    def test_unexpected_error_is_logged(self):
        """Test that unexpected errors are logged"""
        @handle_paystack_errors
        def my_view():
            raise RuntimeError("boom")

        import logging
        with patch.object(logging.getLogger('djpaystack'), 'exception') as mock_log:
            my_view()
            mock_log.assert_called_once()
