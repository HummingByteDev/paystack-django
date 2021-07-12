from django.db import models
import secrets
from pay.paystack import Paystack


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    ref = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    verified = models.BooleanField(default=False)
    payment_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-payment_date',)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(15)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] == self.amount:
                self.verified = True
                self.save()
        if self.verified:
            return True
        return False
