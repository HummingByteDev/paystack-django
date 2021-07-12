from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from pay.forms import PaymentForm
from django.contrib import messages
from pay.models import Payment


def initiate_payment(request):
    if request.method == "POST":
        payment_form = PaymentForm(request.POST or None)
        if payment_form.is_valid():
            payment = payment_form.save()
            return render(request, 'make-payment.html',
                          {'payment': payment, 'paystack_public_key': settings.PAYSTACK_TEST_PUBLIC_KEY})
    else:
        payment_form = PaymentForm()
    return render(request, 'initiate-payment.html', {'payment_form': payment_form})


def verify_payment(request, ref):
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, "Payment Verified")  # Send a mail
    else:
        messages.error(request, "Payment Varification Failed")
    return redirect('initiate-payment')
