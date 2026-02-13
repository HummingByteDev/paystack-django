from typing import Dict, Any, Optional, List
from .base import BaseAPI


class MiscellaneousAPI(BaseAPI):
    """Miscellaneous API"""

    def list_banks(self, country: str = 'nigeria', use_cursor: bool = False,
                   per_page: int = 50, page: Optional[int] = None,
                   pay_with_bank_transfer: Optional[bool] = None,
                   pay_with_bank: Optional[bool] = None, enabled_for_verification: Optional[bool] = None,
                   type: Optional[str] = None, currency: Optional[str] = None) -> Dict[str, Any]:
        """List banks"""
        params = self._build_query_params(
            country=country, use_cursor=use_cursor, pay_with_bank_transfer=pay_with_bank_transfer,
            pay_with_bank=pay_with_bank, enabled_for_verification=enabled_for_verification,
            type=type, currency=currency
        )
        return self._paginate('bank', params=params, per_page=per_page, page=page)

    def list_providers(self, pay_with_bank_transfer: Optional[bool] = None) -> Dict[str, Any]:
        """List providers"""
        params = self._build_query_params(
            pay_with_bank_transfer=pay_with_bank_transfer)
        return self._get('bank', params=params)

    def list_countries(self) -> Dict[str, Any]:
        """List countries"""
        return self._get('country')

    def list_states(self, country: Optional[int] = None) -> Dict[str, Any]:
        """List states"""
        params = self._build_query_params(country=country)
        return self._get('address_verification/states', params=params)
