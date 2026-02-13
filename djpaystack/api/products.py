from typing import Dict, Any, Optional
from .base import BaseAPI


class ProductAPI(BaseAPI):
    """Products API"""

    def create(self, name: str, description: str, price: int, currency: str,
               unlimited: Optional[bool] = None, quantity: Optional[int] = None) -> Dict[str, Any]:
        """Create product"""
        data = self._build_query_params(
            name=name, description=description, price=price, currency=currency,
            unlimited=unlimited, quantity=quantity
        )
        return self._post('product', data=data)

    def list(self, per_page: int = 50, page: Optional[int] = None,
             from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict[str, Any]:
        """List products"""
        params = self._build_query_params(from_date=from_date, to_date=to_date)
        return self._paginate('product', params=params, per_page=per_page, page=page)

    def fetch(self, id: str) -> Dict[str, Any]:
        """Fetch product"""
        return self._get(f'product/{id}')

    def update(self, id: str, name: Optional[str] = None, description: Optional[str] = None,
               price: Optional[int] = None, currency: Optional[str] = None,
               unlimited: Optional[bool] = None, quantity: Optional[int] = None) -> Dict[str, Any]:
        """Update product"""
        data = self._build_query_params(
            name=name, description=description, price=price, currency=currency,
            unlimited=unlimited, quantity=quantity
        )
        return self._put(f'product/{id}', data=data)
