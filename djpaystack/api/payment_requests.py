from typing import Dict, Any, Optional, List
from .base import BaseAPI


class PaymentRequestAPI(BaseAPI):
    """Payment Requests API"""

    def create(self, customer: str, amount: int, due_date: Optional[str] = None,
               description: Optional[str] = None, line_items: Optional[List] = None,
               tax: Optional[List] = None, currency: Optional[str] = None,
               send_notification: Optional[bool] = None, draft: Optional[bool] = None,
               has_invoice: Optional[bool] = None, invoice_number: Optional[int] = None,
               split_code: Optional[str] = None) -> Dict[str, Any]:
        """Create payment request"""
        data = self._build_query_params(
            customer=customer, amount=amount, due_date=due_date, description=description,
            line_items=line_items, tax=tax, currency=currency, send_notification=send_notification,
            draft=draft, has_invoice=has_invoice, invoice_number=invoice_number, split_code=split_code
        )
        return self._post('paymentrequest', data=data)

    def list(self, per_page: int = 50, page: Optional[int] = None,
             customer: Optional[int] = None, status: Optional[str] = None,
             currency: Optional[str] = None, include_archive: Optional[bool] = None,
             from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict[str, Any]:
        """List payment requests"""
        params = self._build_query_params(
            customer=customer, status=status, currency=currency,
            include_archive=include_archive, from_date=from_date, to_date=to_date
        )
        return self._paginate('paymentrequest', params=params, per_page=per_page, page=page)

    def fetch(self, id_or_code: str) -> Dict[str, Any]:
        """Fetch payment request"""
        return self._get(f'paymentrequest/{id_or_code}')

    def verify(self, code: str) -> Dict[str, Any]:
        """Verify payment request"""
        return self._get(f'paymentrequest/verify/{code}')

    def send_notification(self, code: str) -> Dict[str, Any]:
        """Send notification for payment request"""
        return self._post(f'paymentrequest/notify/{code}', data={})

    def total(self) -> Dict[str, Any]:
        """Get payment request totals"""
        return self._get('paymentrequest/totals')

    def finalize(self, code: str) -> Dict[str, Any]:
        """Finalize payment request"""
        return self._post(f'paymentrequest/finalize/{code}', data={})

    def update(self, id_or_code: str, customer: Optional[str] = None, amount: Optional[int] = None,
               currency: Optional[str] = None, due_date: Optional[str] = None,
               description: Optional[str] = None, line_items: Optional[List] = None,
               tax: Optional[List] = None, send_notification: Optional[bool] = None,
               draft: Optional[bool] = None) -> Dict[str, Any]:
        """Update payment request"""
        data = self._build_query_params(
            customer=customer, amount=amount, currency=currency, due_date=due_date,
            description=description, line_items=line_items, tax=tax,
            send_notification=send_notification, draft=draft
        )
        return self._put(f'paymentrequest/{id_or_code}', data=data)

    def archive(self, code: str) -> Dict[str, Any]:
        """Archive payment request"""
        return self._post(f'paymentrequest/archive/{code}', data={})
