from typing import Any, Dict, List, Optional

from .base import BaseAPI


class BulkChargeAPI(BaseAPI):
    """Bulk Charges API"""

    def initiate(self, body: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Initiate bulk charge"""
        data = body
        return self._post("bulkcharge", data=data)

    def list(
        self,
        per_page: int = 50,
        page: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List bulk charges"""
        params = self._build_query_params(from_date=from_date, to_date=to_date)
        return self._paginate("bulkcharge", params=params, per_page=per_page, page=page)

    def fetch(self, id_or_code: str) -> Dict[str, Any]:
        """Fetch bulk charge"""
        return self._get(f"bulkcharge/{id_or_code}")

    def fetch_charges(
        self,
        id_or_code: str,
        status: Optional[str] = None,
        per_page: int = 50,
        page: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Fetch charges in a batch"""
        params = self._build_query_params(status=status, from_date=from_date, to_date=to_date)
        return self._paginate(
            f"bulkcharge/{id_or_code}/charges", params=params, per_page=per_page, page=page
        )

    def pause(self, batch_code: str) -> Dict[str, Any]:
        """Pause bulk charge (GET /bulkcharge/pause/{batch_code})"""
        return self._get(f"bulkcharge/pause/{batch_code}")

    def resume(self, batch_code: str) -> Dict[str, Any]:
        """Resume bulk charge (GET /bulkcharge/resume/{batch_code})"""
        return self._get(f"bulkcharge/resume/{batch_code}")
