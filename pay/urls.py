from django.urls import path, include
from pay.views import initiate_payment, verify_payment


urlpatterns = [
    path("", initiate_payment, name='initiate-payment'),
    path('<str:ref>/', verify_payment, name='verify-payment')
]
