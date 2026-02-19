"""
Direct Debit API
https://paystack.com/docs/payments/direct-debit/
"""
from typing import Dict, Any, Optional, List
from .base import BaseAPI


class DirectDebitAPI(BaseAPI):
    """
    Paystack Direct Debit API

    Direct debit allows a business to debit a customer's bank account
    once the customer has given consent via a mandate authorization.
    Currently available for businesses in Nigeria only.
    """

    def initialize_authorization(
        self,
        email: str,
        channel: str = 'direct_debit',
        callback_url: Optional[str] = None,
        account: Optional[Dict[str, str]] = None,
        address: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Initiate a direct debit authorization request.

        The response contains a redirect_url that you redirect the customer
        to give consent to your request.

        Args:
            email: Customer's email address
            channel: Authorization channel (default: 'direct_debit')
            callback_url: URL to redirect customer after consent
            account: Optional dict with 'number' and 'bank_code' to
                     pre-fill customer's bank details
            address: Optional dict with 'state', 'city', 'street' to
                     pre-fill customer's address

        Returns:
            Response containing redirect_url for customer consent
        """
        data = self._build_query_params(
            email=email,
            channel=channel,
            callback_url=callback_url,
            account=account,
            address=address,
        )
        return self._post('customer/authorization/initialize', data=data)

    def verify_authorization(self, reference: str) -> Dict[str, Any]:
        """
        Verify the status of a direct debit authorization.

        Listen to webhook events (direct_debit.authorization.created,
        direct_debit.authorization.active) for real-time status updates.

        Args:
            reference: Reference from the initialization request

        Returns:
            Authorization details including status
        """
        return self._get(f'customer/authorization/verify/{reference}')

    def activation_charge(
        self,
        customer_id: str,
        authorization_id: int,
    ) -> Dict[str, Any]:
        """
        Trigger an activation charge for a single customer whose authorization
        is stuck in a pending status.

        This causes a debit of NGN 50 on the customer's account to confirm
        it can be debited. The amount is refunded after the check.

        Args:
            customer_id: Customer ID or code
            authorization_id: The authorization ID to activate

        Returns:
            Activation charge response
        """
        data = {'authorization_id': authorization_id}
        return self._put(f'customer/{customer_id}/directdebit-activation-charge', data=data)

    def bulk_activation_charge(
        self,
        customer_ids: List[int],
    ) -> Dict[str, Any]:
        """
        Trigger activation charges for multiple customers at once.

        Args:
            customer_ids: List of customer IDs to activate

        Returns:
            Bulk activation charge response
        """
        data = {'customer_ids': customer_ids}
        return self._put('directdebit/activation-charge', data=data)
