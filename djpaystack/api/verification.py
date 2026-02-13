from typing import Dict, Any, Optional
from .base import BaseAPI


class VerificationAPI(BaseAPI):
    """Verification API"""

    def resolve_account_number(self, account_number: str, bank_code: str) -> Dict[str, Any]:
        """Resolve account number"""
        params = {'account_number': account_number, 'bank_code': bank_code}
        return self._get('bank/resolve', params=params)

    def validate_account(self, account_name: str, account_number: str,
                         account_type: str, bank_code: str, country_code: str,
                         document_type: str, document_number: Optional[str] = None) -> Dict[str, Any]:
        """Validate account"""
        data = self._build_query_params(
            account_name=account_name, account_number=account_number,
            account_type=account_type, bank_code=bank_code, country_code=country_code,
            document_type=document_type, document_number=document_number
        )
        return self._post('bank/validate', data=data)

    def resolve_card_bin(self, bin: str) -> Dict[str, Any]:
        """Resolve card BIN"""
        return self._get(f'decision/bin/{bin}')
