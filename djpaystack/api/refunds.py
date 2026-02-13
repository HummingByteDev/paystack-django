from typing import Dict, Any, Optional
from .base import BaseAPI


class RefundAPI(BaseAPI):
    """Refunds API"""

    def create(self, transaction: str, amount: Optional[int] = None,
               currency: Optional[str] = None, customer_note: Optional[str] = None,
               merchant_note: Optional[str] = None) -> Dict[str, Any]:
        """Create refund"""
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
