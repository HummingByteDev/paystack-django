from typing import Any, Dict, List, Optional

from .base import BaseAPI


class TransferAPI(BaseAPI):
    """Transfers API"""

    def initiate(
        self,
        source: str,
        amount: int,
        recipient: str,
        reason: Optional[str] = None,
        currency: Optional[str] = None,
        reference: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Initiate transfer"""
        data = self._build_query_params(
            source=source,
            amount=amount,
            recipient=recipient,
            reason=reason,
            currency=currency,
            reference=reference,
        )
        return self._post("transfer", data=data)

    def finalize(self, transfer_code: str, otp: str) -> Dict[str, Any]:
        """Finalize transfer"""
        data = {"transfer_code": transfer_code, "otp": otp}
        return self._post("transfer/finalize_transfer", data=data)

    def bulk_transfer(self, source: str, transfers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Initiate bulk transfer"""
        data = {"source": source, "transfers": transfers}
        return self._post("transfer/bulk", data=data)

    def list(
        self,
        per_page: int = 50,
        page: Optional[int] = None,
        recipient: Optional[int] = None,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        customer: Optional[int] = None,
    ) -> Dict[str, Any]:
        """List transfers

        the Paystack filter is ``recipient`` (not ``customer``). The
        ``customer`` parameter is retained as a deprecated alias for
        backwards compatibility and is treated as ``recipient`` when set.
        """
        if recipient is None and customer is not None:
            recipient = customer
        params = self._build_query_params(
            recipient=recipient, status=status, from_date=from_date, to_date=to_date
        )
        return self._paginate("transfer", params=params, per_page=per_page, page=page)

    def fetch(self, id_or_code: str) -> Dict[str, Any]:
        """Fetch transfer"""
        return self._get(f"transfer/{id_or_code}")

    def verify(self, reference: str) -> Dict[str, Any]:
        """Verify transfer"""
        return self._get(f"transfer/verify/{reference}")

    def export(
        self,
        recipient: Optional[int] = None,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Export transfers (GET /transfer/export)."""
        params = self._build_query_params(
            recipient=recipient, status=status, from_date=from_date, to_date=to_date
        )
        return self._get("transfer/export", params=params)
