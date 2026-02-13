from typing import Dict, Any, Optional, List
from .base import BaseAPI


class TransferAPI(BaseAPI):
    """Transfers API"""

    def initiate(self, source: str, amount: int, recipient: str, reason: Optional[str] = None,
                 currency: Optional[str] = None, reference: Optional[str] = None) -> Dict[str, Any]:
        """Initiate transfer"""
        data = self._build_query_params(
            source=source, amount=amount, recipient=recipient, reason=reason,
            currency=currency, reference=reference
        )
        return self._post('transfer', data=data)

    def finalize(self, transfer_code: str, otp: str) -> Dict[str, Any]:
        """Finalize transfer"""
        data = {'transfer_code': transfer_code, 'otp': otp}
        return self._post('transfer/finalize_transfer', data=data)

    def bulk_transfer(self, source: str, transfers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Initiate bulk transfer"""
        data = {'source': source, 'transfers': transfers}
        return self._post('transfer/bulk', data=data)

    def list(self, per_page: int = 50, page: Optional[int] = None,
             customer: Optional[int] = None, status: Optional[str] = None,
             from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict[str, Any]:
        """List transfers"""
        params = self._build_query_params(
            customer=customer, status=status, from_date=from_date, to_date=to_date
        )
        return self._paginate('transfer', params=params, per_page=per_page, page=page)

    def fetch(self, id_or_code: str) -> Dict[str, Any]:
        """Fetch transfer"""
        return self._get(f'transfer/{id_or_code}')

    def verify(self, reference: str) -> Dict[str, Any]:
        """Verify transfer"""
        return self._get(f'transfer/verify/{reference}')
