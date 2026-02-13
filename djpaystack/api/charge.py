from typing import Dict, Any, Optional
from .base import BaseAPI


class ChargeAPI(BaseAPI):
    """Charge API"""

    def create(self, email: str, amount: int, bank: Optional[Dict[str, Any]] = None,
               authorization_code: Optional[str] = None, pin: Optional[str] = None,
               metadata: Optional[Dict] = None, reference: Optional[str] = None,
               ussd: Optional[Dict[str, Any]] = None, mobile_money: Optional[Dict[str, Any]] = None,
               device_id: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Create charge"""
        data = self._build_query_params(
            email=email, amount=amount, bank=bank, authorization_code=authorization_code,
            pin=pin, metadata=metadata, reference=reference, ussd=ussd,
            mobile_money=mobile_money, device_id=device_id, **kwargs
        )
        return self._post('charge', data=data)

    def submit_pin(self, pin: str, reference: str) -> Dict[str, Any]:
        """Submit PIN"""
        data = {'pin': pin, 'reference': reference}
        return self._post('charge/submit_pin', data=data)

    def submit_otp(self, otp: str, reference: str) -> Dict[str, Any]:
        """Submit OTP"""
        data = {'otp': otp, 'reference': reference}
        return self._post('charge/submit_otp', data=data)

    def submit_phone(self, phone: str, reference: str) -> Dict[str, Any]:
        """Submit phone"""
        data = {'phone': phone, 'reference': reference}
        return self._post('charge/submit_phone', data=data)

    def submit_birthday(self, birthday: str, reference: str) -> Dict[str, Any]:
        """Submit birthday"""
        data = {'birthday': birthday, 'reference': reference}
        return self._post('charge/submit_birthday', data=data)

    def submit_address(self, address: str, reference: str, city: str, state: str, zipcode: str) -> Dict[str, Any]:
        """Submit address"""
        data = {
            'address': address, 'reference': reference, 'city': city,
            'state': state, 'zipcode': zipcode
        }
        return self._post('charge/submit_address', data=data)

    def check_pending_charge(self, reference: str) -> Dict[str, Any]:
        """Check pending charge"""
        return self._get(f'charge/{reference}')
