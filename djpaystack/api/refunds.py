"""
Refunds API
https://paystack.com/docs/api/refund/
"""
from typing import Dict, Any, Optional
from .base import BaseAPI


class RefundAPI(BaseAPI):
    """
    Paystack Refunds API

    The Refunds API allows you to create and manage refunds for
    previously successful transactions.
    """

    def create(self, transaction: str, amount: Optional[int] = None,
               currency: Optional[str] = None, customer_note: Optional[str] = None,
               merchant_note: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a refund (full or partial).

        Args:
            transaction: Transaction reference or ID
            amount: Amount to refund in subunit. If not provided, full refund.
            currency: Currency code
            customer_note: Note for customer
            merchant_note: Note for merchant records

        Returns:
            Refund details
        """
        data = self._build_query_params(
            transaction=transaction, amount=amount, currency=currency,
            customer_note=customer_note, merchant_note=merchant_note
        )
        return self._post('refund', data=data)

    def list(self, per_page: int = 50, page: Optional[int] = None,
             reference: Optional[str] = None, currency: Optional[str] = None,
             from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict[str, Any]:
        """List refunds"""
        params = self._build_query_params(
            reference=reference, currency=currency, from_date=from_date, to_date=to_date
        )
        return self._paginate('refund', params=params, per_page=per_page, page=page)

    def fetch(self, reference: str) -> Dict[str, Any]:
        """Fetch refund"""
        return self._get(f'refund/{reference}')

    def retry(
        self,
        refund_id: str,
        account_number: str,
        bank_id: str,
        currency: str = 'NGN',
    ) -> Dict[str, Any]:
        """
        Retry a refund that requires customer bank details.

        Use this when a refund status is 'needs-attention' (i.e. when you
        receive a refund.needs-attention webhook event). The customer's
        bank account details are needed to complete the refund.

        Args:
            refund_id: The refund ID
            account_number: Customer's bank account number
            bank_id: Customer's bank ID
            currency: Currency code (default: 'NGN')

        Returns:
            Retried refund details
        """
        data = {
            'refund_account_details': {
                'currency': currency,
                'account_number': account_number,
                'bank_id': bank_id,
            }
        }
        return self._post(f'refund/retry_with_customer_details/{refund_id}', data=data)
