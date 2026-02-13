
from djpaystack.utils import (
    generate_reference,
    naira_to_kobo,
    kobo_to_naira,
    format_amount,
)
from decimal import Decimal


class TestUtils:
    """Test utility functions"""

    def test_generate_reference(self):
        """Test reference generation"""
        ref = generate_reference()
        assert len(ref) > 0
        assert ref.startswith('PS')

        custom_ref = generate_reference(prefix='TEST')
        assert custom_ref.startswith('TEST')

    def test_naira_to_kobo(self):
        """Test naira to kobo conversion"""
        assert naira_to_kobo(100) == 10000
        assert naira_to_kobo(50.50) == 5050
        assert naira_to_kobo(0.01) == 1

    def test_kobo_to_naira(self):
        """Test kobo to naira conversion"""
        assert kobo_to_naira(10000) == Decimal('100.00')
        assert kobo_to_naira(5050) == Decimal('50.50')
        assert kobo_to_naira(1) == Decimal('0.01')

    def test_format_amount(self):
        """Test amount formatting"""
        assert format_amount(10000, 'NGN') == '₦100.00'
        assert format_amount(500050, 'NGN') == '₦5,000.50'
        assert format_amount(10000, 'USD') == '$100.00'
