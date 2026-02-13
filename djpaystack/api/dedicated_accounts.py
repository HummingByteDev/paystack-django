from typing import Dict, Any, Optional
from .base import BaseAPI


class DedicatedAccountAPI(BaseAPI):
    """Dedicated Virtual Accounts API"""

    def create(self, customer: str, preferred_bank: Optional[str] = None,
               subaccount: Optional[str] = None, split_code: Optional[str] = None,
               first_name: Optional[str] = None, last_name: Optional[str] = None,
               phone: Optional[str] = None) -> Dict[str, Any]:
        """Create dedicated virtual account"""
        data = self._build_query_params(
            customer=customer, preferred_bank=preferred_bank, subaccount=subaccount,
            split_code=split_code, first_name=first_name, last_name=last_name, phone=phone
        )
        return self._post('dedicated_account', data=data)

    def list(self, active: Optional[bool] = None, currency: Optional[str] = None,
             per_page: int = 50, page: Optional[int] = None) -> Dict[str, Any]:
        """List dedicated accounts"""
        params = self._build_query_params(active=active, currency=currency)
        return self._paginate('dedicated_account', params=params, per_page=per_page, page=page)

    def fetch(self, dedicated_account_id: str) -> Dict[str, Any]:
        """Fetch dedicated account"""
        return self._get(f'dedicated_account/{dedicated_account_id}')

    def requery(self, account_number: str, provider_slug: str) -> Dict[str, Any]:
        """Requery dedicated account"""
        params = {'account_number': account_number,
                  'provider_slug': provider_slug}
        return self._get('dedicated_account/requery', params=params)

    def deactivate(self, dedicated_account_id: str) -> Dict[str, Any]:
        """Deactivate dedicated account"""
        return self._delete(f'dedicated_account/{dedicated_account_id}')

    def split(self, customer: str, subaccount: Optional[str] = None,
              split_code: Optional[str] = None, preferred_bank: Optional[str] = None) -> Dict[str, Any]:
        """Split dedicated account transaction"""
        data = self._build_query_params(
            customer=customer, subaccount=subaccount, split_code=split_code, preferred_bank=preferred_bank
        )
        return self._post('dedicated_account/split', data=data)

    def remove_split(self, account_number: str) -> Dict[str, Any]:
        """Remove split from dedicated account"""
        data = {'account_number': account_number}
        return self._delete('dedicated_account/split', data=data)

    def available_providers(self) -> Dict[str, Any]:
        """Get available dedicated account providers"""
        return self._get('dedicated_account/available_providers')
