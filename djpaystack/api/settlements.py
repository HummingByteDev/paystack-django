from typing import Dict, Any, Optional
from .base import BaseAPI


class SettlementAPI(BaseAPI):
    """Settlements API"""

    def list(self, per_page: int = 50, page: Optional[int] = None,
             from_date: Optional[str] = None, to_date: Optional[str] = None,
             subaccount: Optional[str] = None) -> Dict[str, Any]:
        """List settlements"""
        params = self._build_query_params(
            from_date=from_date, to_date=to_date, subaccount=subaccount)
        return self._paginate('settlement', params=params, per_page=per_page, page=page)

    def fetch_transactions(self, id: str, per_page: int = 50, page: Optional[int] = None,
                           from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict[str, Any]:
        """Fetch settlement transactions"""
        params = self._build_query_params(from_date=from_date, to_date=to_date)
        return self._paginate(f'settlement/{id}/transactions', params=params, per_page=per_page, page=page)
