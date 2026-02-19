"""
Dedicated Virtual Accounts API
https://paystack.com/docs/api/dedicated-virtual-account/
"""
from typing import Dict, Any, Optional
from .base import BaseAPI


class DedicatedAccountAPI(BaseAPI):
    """
    Paystack Dedicated Virtual Accounts API

    Create and manage bank accounts for your customers. Bank transfers to these
    accounts are automatically recorded as transactions from that customer.
    Available to registered businesses in Nigeria and Ghana.
    """

    def create(self, customer: str, preferred_bank: Optional[str] = None,
               subaccount: Optional[str] = None, split_code: Optional[str] = None,
               first_name: Optional[str] = None, last_name: Optional[str] = None,
               phone: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a dedicated virtual account (multi-step flow).

        The customer must already exist. For Nigerian businesses in
        Betting/Financial/General services categories, the customer must
        be validated first.

        Args:
            customer: Customer ID or code
            preferred_bank: Bank slug (e.g. 'wema-bank', 'titan-paystack', 'test-bank')
            subaccount: Subaccount code for split payments
            split_code: Split code for multi-split payments
            first_name: Customer's first name
            last_name: Customer's last name
            phone: Customer's phone number

        Returns:
            Dedicated account details
        """
        data = self._build_query_params(
            customer=customer, preferred_bank=preferred_bank, subaccount=subaccount,
            split_code=split_code, first_name=first_name, last_name=last_name, phone=phone
        )
        return self._post('dedicated_account', data=data)

    def assign(
        self,
        email: str,
        first_name: str,
        last_name: str,
        phone: str,
        preferred_bank: str,
        country: str = 'NG',
        middle_name: Optional[str] = None,
        account_number: Optional[str] = None,
        bvn: Optional[str] = None,
        bank_code: Optional[str] = None,
        subaccount: Optional[str] = None,
        split_code: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create and assign a dedicated virtual account in a single step.

        Handles customer creation, optional validation, and DVA assignment.
        For businesses in Betting/Financial/General services categories,
        account_number, bvn, and bank_code are required for compliance.

        Args:
            email: Customer's email address
            first_name: Customer's first name
            last_name: Customer's last name
            phone: Customer's phone number
            preferred_bank: Bank slug (e.g. 'wema-bank', 'titan-paystack', 'test-bank')
            country: Customer's country (default: 'NG')
            middle_name: Customer's middle name
            account_number: Customer's bank account number (compliance)
            bvn: Customer's BVN (compliance)
            bank_code: Customer's bank code (compliance)
            subaccount: Subaccount code for split payments
            split_code: Split code for multi-split payments

        Returns:
            Assignment response (listen for dedicatedaccount.assign.success webhook)
        """
        data = self._build_query_params(
            email=email, first_name=first_name, last_name=last_name,
            phone=phone, preferred_bank=preferred_bank, country=country,
            middle_name=middle_name, account_number=account_number,
            bvn=bvn, bank_code=bank_code, subaccount=subaccount,
            split_code=split_code,
        )
        return self._post('dedicated_account/assign', data=data)

    def list(self, active: Optional[bool] = None, currency: Optional[str] = None,
             per_page: int = 50, page: Optional[int] = None) -> Dict[str, Any]:
        """List dedicated accounts"""
        params = self._build_query_params(active=active, currency=currency)
        return self._paginate('dedicated_account', params=params, per_page=per_page, page=page)

    def fetch(self, dedicated_account_id: str) -> Dict[str, Any]:
        """Fetch dedicated account"""
        return self._get(f'dedicated_account/{dedicated_account_id}')

    def requery(self, account_number: str, provider_slug: str,
                date: Optional[str] = None) -> Dict[str, Any]:
        """
        Requery a dedicated account for pending transactions.

        Rate limited to once every 10 minutes per account.

        Args:
            account_number: Virtual account number
            provider_slug: Provider slug
            date: Date to check in YYYY-MM-DD format

        Returns:
            Requery response
        """
        params = self._build_query_params(
            account_number=account_number,
            provider_slug=provider_slug,
            date=date,
        )
        return self._get('dedicated_account/requery', params=params)

    def deactivate(self, dedicated_account_id: str) -> Dict[str, Any]:
        """Deactivate dedicated account"""
        return self._delete(f'dedicated_account/{dedicated_account_id}')

    def split(self, account_number: str, subaccount: Optional[str] = None,
              split_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Add or update a subaccount/split on an existing dedicated virtual account.

        Args:
            account_number: The dedicated virtual account number
            subaccount: Subaccount code for split payments
            split_code: Split code for multi-split payments

        Returns:
            Updated split configuration
        """
        data = self._build_query_params(
            account_number=account_number, subaccount=subaccount,
            split_code=split_code,
        )
        return self._post('dedicated_account/split', data=data)

    def remove_split(self, account_number: str) -> Dict[str, Any]:
        """Remove split from dedicated account"""
        data = {'account_number': account_number}
        return self._delete('dedicated_account/split', data=data)

    def available_providers(self) -> Dict[str, Any]:
        """Get available dedicated account providers (banks)"""
        return self._get('dedicated_account/available_providers')
