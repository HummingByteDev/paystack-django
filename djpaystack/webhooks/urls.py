from django.urls import path
from .views import PaystackWebhookView

app_name = 'djpaystack'

urlpatterns = [
    path('webhook/', PaystackWebhookView.as_view(), name='webhook'),
]
