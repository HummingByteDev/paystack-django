from typing import Dict, Any, Optional
from .base import BaseAPI


class SubscriptionAPI(BaseAPI):
    """Subscriptions API"""

    def create(self, customer: str, plan: str, authorization: Optional[str] = None,
               start_date: Optional[str] = None) -> Dict[str, Any]:
        """Create subscription"""
        data = self._build_query_params(
            customer=customer, plan=plan, authorization=authorization, start_date=start_date
        )
        return self._post('subscription', data=data)

    def list(self, per_page: int = 50, page: Optional[int] = None,
             customer: Optional[int] = None, plan: Optional[int] = None) -> Dict[str, Any]:
        """List subscriptions"""
        params = self._build_query_params(customer=customer, plan=plan)
        return self._paginate('subscription', params=params, per_page=per_page, page=page)

    def fetch(self, id_or_code: str) -> Dict[str, Any]:
        """Fetch subscription"""
        return self._get(f'subscription/{id_or_code}')

    def enable(self, code: str, token: str) -> Dict[str, Any]:
        """Enable subscription"""
        data = {'code': code, 'token': token}
        return self._post('subscription/enable', data=data)

    def disable(self, code: str, token: str) -> Dict[str, Any]:
        """Disable subscription"""
        data = {'code': code, 'token': token}
        return self._post('subscription/disable', data=data)

    def generate_update_link(self, code: str) -> Dict[str, Any]:
        """Generate update subscription link"""
        return self._get(f'subscription/{code}/manage/link')

    def send_update_link(self, code: str) -> Dict[str, Any]:
        """Send update subscription link"""
        return self._post(f'subscription/{code}/manage/email', data={})
