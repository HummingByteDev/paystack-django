from typing import Dict, Any, Optional
from .base import BaseAPI


class SubaccountAPI(BaseAPI):
    """Subaccounts API"""

    def create(self, business_name: str, settlement_bank: str, account_number: str,
               percentage_charge: float, description: Optional[str] = None,
               primary_contact_email: Optional[str] = None, primary_contact_name: Optional[str] = None,
               primary_contact_phone: Optional[str] = None, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Create subaccount"""
        data = self._build_query_params(
            business_name=business_name, settlement_bank=settlement_bank,
            account_number=account_number, percentage_charge=percentage_charge,
            description=description, primary_contact_email=primary_contact_email,
            primary_contact_name=primary_contact_name, primary_contact_phone=primary_contact_phone,
            metadata=metadata
        )
        return self._post('subaccount', data=data)

    def list(self, per_page: int = 50, page: Optional[int] = None,
             from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict[str, Any]:
        """List subaccounts"""
        params = self._build_query_params(from_date=from_date, to_date=to_date)
        return self._paginate('subaccount', params=params, per_page=per_page, page=page)

    def fetch(self, id_or_code: str) -> Dict[str, Any]:
        """Fetch subaccount"""
        return self._get(f'subaccount/{id_or_code}')

    def update(self, id_or_code: str, business_name: Optional[str] = None,
               settlement_bank: Optional[str] = None, account_number: Optional[str] = None,
               percentage_charge: Optional[float] = None, description: Optional[str] = None,
               primary_contact_email: Optional[str] = None, primary_contact_name: Optional[str] = None,
               primary_contact_phone: Optional[str] = None, settlement_schedule: Optional[str] = None,
               active: Optional[bool] = None, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Update subaccount"""
        data = self._build_query_params(
            business_name=business_name, settlement_bank=settlement_bank,
            account_number=account_number, percentage_charge=percentage_charge,
            description=description, primary_contact_email=primary_contact_email,
            primary_contact_name=primary_contact_name, primary_contact_phone=primary_contact_phone,
            settlement_schedule=settlement_schedule, active=active, metadata=metadata
        )
        return self._put(f'subaccount/{id_or_code}', data=data)
