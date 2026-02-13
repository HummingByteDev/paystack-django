from typing import Dict, Any, Optional, List
from .base import BaseAPI


class SplitAPI(BaseAPI):
    """Transaction Splits API"""

    def create(
        self,
        name: str,
        type: str,
        currency: str,
        subaccounts: List[Dict[str, Any]],
        bearer_type: str,
        bearer_subaccount: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a split"""
        data = self._build_query_params(
            name=name,
            type=type,
            currency=currency,
            subaccounts=subaccounts,
            bearer_type=bearer_type,
            bearer_subaccount=bearer_subaccount,
            **kwargs
        )
        return self._post('split', data=data)

    def list(self, name: Optional[str] = None, active: Optional[bool] = None,
             sort_by: Optional[str] = None, per_page: int = 50,
             page: Optional[int] = None) -> Dict[str, Any]:
        """List splits"""
        params = self._build_query_params(
            name=name, active=active, sort_by=sort_by)
        return self._paginate('split', params=params, per_page=per_page, page=page)

    def fetch(self, id: str) -> Dict[str, Any]:
        """Fetch a split"""
        return self._get(f'split/{id}')

    def update(self, id: str, name: Optional[str] = None, active: Optional[bool] = None,
               bearer_type: Optional[str] = None, bearer_subaccount: Optional[str] = None) -> Dict[str, Any]:
        """Update a split"""
        data = self._build_query_params(
            name=name, active=active, bearer_type=bearer_type, bearer_subaccount=bearer_subaccount
        )
        return self._put(f'split/{id}', data=data)

    def add_subaccount(self, id: str, subaccount: str, share: int) -> Dict[str, Any]:
        """Add subaccount to split"""
        data = {'subaccount': subaccount, 'share': share}
        return self._post(f'split/{id}/subaccount/add', data=data)

    def remove_subaccount(self, id: str, subaccount: str) -> Dict[str, Any]:
        """Remove subaccount from split"""
        data = {'subaccount': subaccount}
        return self._post(f'split/{id}/subaccount/remove', data=data)
