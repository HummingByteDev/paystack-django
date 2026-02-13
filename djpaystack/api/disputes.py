from typing import Dict, Any, Optional
from .base import BaseAPI


class DisputeAPI(BaseAPI):
    """Disputes API"""

    def list(self, per_page: int = 50, page: Optional[int] = None,
             from_date: Optional[str] = None, to_date: Optional[str] = None,
             transaction: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """List disputes"""
        params = self._build_query_params(
            from_date=from_date, to_date=to_date, transaction=transaction, status=status
        )
        return self._paginate('dispute', params=params, per_page=per_page, page=page)

    def fetch(self, id: str) -> Dict[str, Any]:
        """Fetch dispute"""
        return self._get(f'dispute/{id}')

    def list_transaction_disputes(self, id: str) -> Dict[str, Any]:
        """List transaction disputes"""
        return self._get(f'dispute/transaction/{id}')

    def update(self, id: str, refund_amount: int, uploaded_filename: Optional[str] = None) -> Dict[str, Any]:
        """Update dispute"""
        data = self._build_query_params(
            refund_amount=refund_amount, uploaded_filename=uploaded_filename)
        return self._put(f'dispute/{id}', data=data)

    def add_evidence(self, id: str, customer_email: str, customer_name: str,
                     customer_phone: str, service_details: str,
                     delivery_address: Optional[str] = None, delivery_date: Optional[str] = None) -> Dict[str, Any]:
        """Add evidence to dispute"""
        data = self._build_query_params(
            customer_email=customer_email, customer_name=customer_name,
            customer_phone=customer_phone, service_details=service_details,
            delivery_address=delivery_address, delivery_date=delivery_date
        )
        return self._post(f'dispute/{id}/evidence', data=data)

    def get_upload_url(self, id: str, upload_filename: str) -> Dict[str, Any]:
        """Get upload URL for dispute evidence"""
        params = {'upload_filename': upload_filename}
        return self._get(f'dispute/{id}/upload_url', params=params)

    def resolve(self, id: str, resolution: str, message: str, refund_amount: int,
                uploaded_filename: str, evidence: Optional[int] = None) -> Dict[str, Any]:
        """Resolve dispute"""
        data = self._build_query_params(
            resolution=resolution, message=message, refund_amount=refund_amount,
            uploaded_filename=uploaded_filename, evidence=evidence
        )
        return self._put(f'dispute/{id}/resolve', data=data)

    def export(self, per_page: int = 50, page: Optional[int] = None,
               from_date: Optional[str] = None, to_date: Optional[str] = None,
               transaction: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """Export disputes"""
        params = self._build_query_params(
            perPage=per_page, page=page, from_date=from_date, to_date=to_date,
            transaction=transaction, status=status
        )
        return self._get('dispute/export', params=params)
