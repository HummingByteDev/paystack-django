from typing import Dict, Any
from .base import BaseAPI


class TransferControlAPI(BaseAPI):
    """Transfers Control API"""

    def check_balance(self) -> Dict[str, Any]:
        """Check balance"""
        return self._get('balance')

    def fetch_balance_ledger(self) -> Dict[str, Any]:
        """Fetch balance ledger"""
        return self._get('balance/ledger')

    def resend_otp(self, transfer_code: str, reason: str) -> Dict[str, Any]:
        """Resend OTP for transfer"""
        data = {'transfer_code': transfer_code, 'reason': reason}
        return self._post('transfer/resend_otp', data=data)

    def disable_otp(self) -> Dict[str, Any]:
        """Disable OTP requirement for transfers"""
        return self._post('transfer/disable_otp', data={})

    def finalize_disable_otp(self, otp: str) -> Dict[str, Any]:
        """Finalize OTP disable"""
        data = {'otp': otp}
        return self._post('transfer/disable_otp_finalize', data=data)

    def enable_otp(self) -> Dict[str, Any]:
        """Enable OTP requirement for transfers"""
        return self._post('transfer/enable_otp', data={})
