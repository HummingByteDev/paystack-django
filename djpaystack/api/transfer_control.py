from typing import Any, Dict, Optional

from .base import BaseAPI


class TransferControlAPI(BaseAPI):
    """Transfers Control API"""

    def check_balance(self) -> Dict[str, Any]:
        """Check balance"""
        return self._get("balance")

    def fetch_balance_ledger(
        self,
        per_page: int = 50,
        page: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Fetch balance ledger (now supports pagination + date filters)."""
        params = self._build_query_params(
            perPage=per_page, page=page, from_date=from_date, to_date=to_date
        )
        return self._get("balance/ledger", params=params)

    def resend_otp(self, transfer_code: str, reason: str) -> Dict[str, Any]:
        """Resend OTP for transfer"""
        data = {"transfer_code": transfer_code, "reason": reason}
        return self._post("transfer/resend_otp", data=data)

    def disable_otp(self) -> Dict[str, Any]:
        """Disable OTP requirement for transfers"""
        return self._post("transfer/disable_otp", data={})

    def finalize_disable_otp(self, otp: str) -> Dict[str, Any]:
        """Finalize OTP disable"""
        data = {"otp": otp}
        return self._post("transfer/disable_otp_finalize", data=data)

    def enable_otp(self) -> Dict[str, Any]:
        """Enable OTP requirement for transfers"""
        return self._post("transfer/enable_otp", data={})
