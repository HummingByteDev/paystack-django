from typing import Dict, Any, Optional
from .base import BaseAPI


class DirectDebitAPI(BaseAPI):
    """Direct Debit API"""

    def activate_mandate(self, mandate_id: str) -> Dict[str, Any]:
        """Activate a mandate"""
        return self._post(f'mandate/{mandate_id}/activate', data={})

    def fetch_mandate(self, mandate_id: str) -> Dict[str, Any]:
        """Fetch mandate"""
        return self._get(f'mandate/{mandate_id}')

    def list_mandates(self, per_page: int = 50, page: Optional[int] = None) -> Dict[str, Any]:
        """List mandates"""
        return self._paginate('mandate', per_page=per_page, page=page)

    def deactivate_mandate(self, mandate_id: str) -> Dict[str, Any]:
        """Deactivate mandate"""
        return self._post(f'mandate/{mandate_id}/deactivate', data={})
