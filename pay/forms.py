from django import forms
from pay.models import Payment


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ("amount", "email")
