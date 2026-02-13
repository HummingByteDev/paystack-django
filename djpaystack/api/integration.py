from typing import Dict, Any
from .base import BaseAPI


class IntegrationAPI(BaseAPI):
    """Integration API"""

    def fetch_timeout(self) -> Dict[str, Any]:
        """Fetch payment session timeout"""
        return self._get('integration/payment_session_timeout')

    def update_timeout(self, timeout: int) -> Dict[str, Any]:
        """Update payment session timeout"""
        data = {'timeout': timeout}
        return self._put('integration/payment_session_timeout', data=data)
