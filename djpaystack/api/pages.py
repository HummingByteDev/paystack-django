from typing import Dict, Any, Optional, List
from .base import BaseAPI


class PageAPI(BaseAPI):
    """Payment Pages API"""

    def create(self, name: str, description: Optional[str] = None, amount: Optional[int] = None,
               slug: Optional[str] = None, metadata: Optional[Dict] = None,
               redirect_url: Optional[str] = None, custom_fields: Optional[List] = None) -> Dict[str, Any]:
        """Create payment page"""
        data = self._build_query_params(
            name=name, description=description, amount=amount, slug=slug,
            metadata=metadata, redirect_url=redirect_url, custom_fields=custom_fields
        )
        return self._post('page', data=data)

    def list(self, per_page: int = 50, page: Optional[int] = None,
             from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict[str, Any]:
        """List payment pages"""
        params = self._build_query_params(from_date=from_date, to_date=to_date)
        return self._paginate('page', params=params, per_page=per_page, page=page)

    def fetch(self, id_or_slug: str) -> Dict[str, Any]:
        """Fetch payment page"""
        return self._get(f'page/{id_or_slug}')

    def update(self, id_or_slug: str, name: Optional[str] = None, description: Optional[str] = None,
               amount: Optional[int] = None, active: Optional[bool] = None) -> Dict[str, Any]:
        """Update payment page"""
        data = self._build_query_params(
            name=name, description=description, amount=amount, active=active)
        return self._put(f'page/{id_or_slug}', data=data)

    def check_slug_availability(self, slug: str) -> Dict[str, Any]:
        """Check if slug is available"""
        return self._get(f'page/check_slug_availability/{slug}')

    def add_products(self, id: str, product: List[int]) -> Dict[str, Any]:
        """Add products to payment page"""
        data = {'product': product}
        return self._post(f'page/{id}/product', data=data)
