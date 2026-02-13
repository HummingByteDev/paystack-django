from typing import Dict, Any, Optional
from .base import BaseAPI


class ApplePayAPI(BaseAPI):
    """Apple Pay API"""

    def register_domain(self, domainName: str) -> Dict[str, Any]:
        """Register domain for Apple Pay"""
        data = {'domainName': domainName}
        return self._post('apple-pay/domain', data=data)

    def list_domains(self, use_cursor: bool = False, per_page: int = 50,
                     page: Optional[int] = None) -> Dict[str, Any]:
        """List Apple Pay domains"""
        params = self._build_query_params(use_cursor=use_cursor)
        return self._paginate('apple-pay/domain', params=params, per_page=per_page, page=page)

    def unregister_domain(self, domainName: str) -> Dict[str, Any]:
        """Unregister Apple Pay domain"""
        data = {'domainName': domainName}
        return self._delete('apple-pay/domain', data=data)
