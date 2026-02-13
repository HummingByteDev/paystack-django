from typing import Dict, Any, Optional
from .base import BaseAPI


class PlanAPI(BaseAPI):
    """Plans API"""

    def create(self, name: str, amount: int, interval: str,
               description: Optional[str] = None, currency: Optional[str] = None,
               invoice_limit: Optional[int] = None, send_invoices: Optional[bool] = None,
               send_sms: Optional[bool] = None) -> Dict[str, Any]:
        """Create plan"""
        data = self._build_query_params(
            name=name, amount=amount, interval=interval, description=description,
            currency=currency, invoice_limit=invoice_limit, send_invoices=send_invoices,
            send_sms=send_sms
        )
        return self._post('plan', data=data)

    def list(self, per_page: int = 50, page: Optional[int] = None,
             status: Optional[str] = None, interval: Optional[str] = None,
             amount: Optional[int] = None) -> Dict[str, Any]:
        """List plans"""
        params = self._build_query_params(
            status=status, interval=interval, amount=amount)
        return self._paginate('plan', params=params, per_page=per_page, page=page)

    def fetch(self, id_or_code: str) -> Dict[str, Any]:
        """Fetch plan"""
        return self._get(f'plan/{id_or_code}')

    def update(self, id_or_code: str, name: Optional[str] = None, amount: Optional[int] = None,
               interval: Optional[str] = None, description: Optional[str] = None,
               currency: Optional[str] = None, invoice_limit: Optional[int] = None,
               send_invoices: Optional[bool] = None, send_sms: Optional[bool] = None) -> Dict[str, Any]:
        """Update plan"""
        data = self._build_query_params(
            name=name, amount=amount, interval=interval, description=description,
            currency=currency, invoice_limit=invoice_limit, send_invoices=send_invoices,
            send_sms=send_sms
        )
        return self._put(f'plan/{id_or_code}', data=data)
