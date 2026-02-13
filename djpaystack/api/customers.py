"""
Customers API
https://paystack.com/docs/api/customer/
"""
from typing import Dict, Any, Optional
from .base import BaseAPI


class CustomerAPI(BaseAPI):
    """
    Paystack Customers API
    
    The Customers API allows you create and manage customers on your integration.
    """
    
    def create(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a customer
        
        Args:
            email: Customer's email address
            first_name: Customer's first name
            last_name: Customer's last name
            phone: Customer's phone number
            metadata: Additional customer data
            
        Returns:
            Created customer data
        """
        data = self._build_query_params(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            metadata=metadata,
            **kwargs
        )
        return self._post('customer', data=data)
    
    def list(
        self,
        per_page: int = 50,
        page: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List customers
        
        Args:
            per_page: Records per page
            page: Page number
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            
        Returns:
            List of customers
        """
        params = self._build_query_params(
            from_date=from_date,
            to_date=to_date
        )
        return self._paginate('customer', params=params, per_page=per_page, page=page)
    
    def fetch(self, email_or_code: str) -> Dict[str, Any]:
        """
        Fetch a customer
        
        Args:
            email_or_code: Customer email or customer code
            
        Returns:
            Customer details
        """
        return self._get(f'customer/{email_or_code}')
    
    def update(
        self,
        code: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update a customer
        
        Args:
            code: Customer code
            first_name: Customer's first name
            last_name: Customer's last name
            phone: Customer's phone number
            metadata: Additional customer data
            
        Returns:
            Updated customer data
        """
        data = self._build_query_params(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            metadata=metadata,
            **kwargs
        )
        return self._put(f'customer/{code}', data=data)
    
    def validate(
        self,
        code: str,
        first_name: str,
        last_name: str,
        type: str,
        value: str,
        country: str,
        bvn: Optional[str] = None,
        bank_code: Optional[str] = None,
        account_number: Optional[str] = None,
        middle_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate a customer's identity
        
        Args:
            code: Customer code
            first_name: Customer's first name
            last_name: Customer's last name
            type: Identification type (bvn, bank_account)
            value: Identification value
            country: Country code (NG, GH)
            bvn: Bank Verification Number
            bank_code: Customer's bank code
            account_number: Customer's account number
            middle_name: Customer's middle name
            
        Returns:
            Validation response
        """
        data = self._build_query_params(
            first_name=first_name,
            last_name=last_name,
            type=type,
            value=value,
            country=country,
            bvn=bvn,
            bank_code=bank_code,
            account_number=account_number,
            middle_name=middle_name
        )
        return self._post(f'customer/{code}/identification', data=data)
    
    def set_risk_action(
        self,
        customer: str,
        risk_action: str
    ) -> Dict[str, Any]:
        """
        Whitelist or blacklist a customer
        
        Args:
            customer: Customer code or email
            risk_action: Action to take (default, allow, deny)
            
        Returns:
            Response data
        """
        data = {
            'customer': customer,
            'risk_action': risk_action
        }
        return self._post('customer/set_risk_action', data=data)
    
    def deactivate_authorization(
        self,
        authorization_code: str
    ) -> Dict[str, Any]:
        """
        Deactivate an authorization
        
        Args:
            authorization_code: Authorization code to deactivate
            
        Returns:
            Response data
        """
        data = {'authorization_code': authorization_code}
        return self._post('customer/deactivate_authorization', data=data)