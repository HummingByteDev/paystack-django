from typing import Dict, Any, Optional, List
from .base import BaseAPI


class TransferRecipientAPI(BaseAPI):
    """Transfer Recipients API"""

    def create(self, type: str, name: str, account_number: str, bank_code: str,
               description: Optional[str] = None, currency: Optional[str] = None,
               authorization_code: Optional[str] = None, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Create transfer recipient"""
        data = self._build_query_params(
            type=type, name=name, account_number=account_number, bank_code=bank_code,
            description=description, currency=currency, authorization_code=authorization_code,
            metadata=metadata
        )
        return self._post('transferrecipient', data=data)

    def bulk_create(self, batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple transfer recipients"""
        data = {'batch': batch}
        return self._post('transferrecipient/bulk', data=data)

    def list(self, per_page: int = 50, page: Optional[int] = None,
             from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict[str, Any]:
        """List transfer recipients"""
        params = self._build_query_params(from_date=from_date, to_date=to_date)
        return self._paginate('transferrecipient', params=params, per_page=per_page, page=page)

    def fetch(self, id_or_code: str) -> Dict[str, Any]:
        """Fetch transfer recipient"""
        return self._get(f'transferrecipient/{id_or_code}')

    def update(self, id_or_code: str, name: Optional[str] = None, email: Optional[str] = None) -> Dict[str, Any]:
        """Update transfer recipient"""
        data = self._build_query_params(name=name, email=email)
        return self._put(f'transferrecipient/{id_or_code}', data=data)

    def delete(self, id_or_code: str) -> Dict[str, Any]:
        """Delete transfer recipient"""
        return self._delete(f'transferrecipient/{id_or_code}')
