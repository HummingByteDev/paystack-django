.. _advanced/webhooks:

Advanced Webhook Handling
=========================

Beyond basic webhook setup, here are advanced patterns and best practices.

Webhook Signature Verification
------------------------------

Always verify webhook signatures to ensure requests are from Paystack:

.. code-block:: python

    from djpaystack.webhooks.handlers import verify_webhook_signature
    from django.http import JsonResponse
    from django.views.decorators.http import require_http_methods
    import json

    @require_http_methods(["POST"])
    def webhook_with_verification(request):
        """Webhook with signature verification"""
        
        # Get the webhook secret from settings
        from django.conf import settings
        webhook_secret = settings.PAYSTACK.get('WEBHOOK_SECRET')
        
        # Verify signature
        if not verify_webhook_signature(request, webhook_secret):
            return JsonResponse({'error': 'Invalid signature'}, status=401)
        
        # Process the webhook
        try:
            payload = json.loads(request.body)
            event = payload.get('event')
            
            if event == 'charge.success':
                handle_charge_success(payload['data'])
            elif event == 'charge.failed':
                handle_charge_failed(payload['data'])
            
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

Idempotent Processing
---------------------

Process webhooks idempotently so duplicate events don't cause issues:

.. code-block:: python

    from django.db import models
    from django.db.models import Q
    import uuid

    class WebhookEvent(models.Model):
        """Track processed webhook events"""
        event_id = models.CharField(max_length=255, unique=True)
        event = models.CharField(max_length=100)
        data = models.JSONField()
        processed = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)

    def process_webhook(payload):
        """Process webhook idempotently"""
        event_id = payload.get('id')
        
        # Check if already processed
        try:
            webhook_event = WebhookEvent.objects.get(event_id=event_id)
            if webhook_event.processed:
                return  # Already processed
        except WebhookEvent.DoesNotExist:
            webhook_event = WebhookEvent.objects.create(
                event_id=event_id,
                event=payload.get('event'),
                data=payload.get('data', {})
            )
        
        # Process the event
        try:
            handle_event(payload)
            webhook_event.processed = True
            webhook_event.save()
        except Exception as e:
            # Retry on next attempt
            raise

Async Webhook Processing
------------------------

Use Celery for async webhook processing to avoid timeouts:

.. code-block:: python

    from celery import shared_task
    from django.http import JsonResponse
    from django.views.decorators.http import require_http_methods
    import json

    @shared_task
    def process_webhook_async(event, data):
        """Process webhook asynchronously"""
        if event == 'charge.success':
            handle_charge_success(data)
        elif event == 'charge.failed':
            handle_charge_failed(data)
        # ... other event handlers

    @require_http_methods(["POST"])
    def webhook_async(request):
        """Async webhook handler"""
        payload = json.loads(request.body)
        
        # Queue for async processing
        process_webhook_async.delay(
            payload.get('event'),
            payload.get('data')
        )
        
        # Return immediately
        return JsonResponse({'status': 'received'})

Webhook Retry Logic
-------------------

Implement retry logic for failed webhook processing:

.. code-block:: python

    from django.db import models
    from django.utils import timezone
    from django.core.exceptions import ValidationError
    import json

    class WebhookLog(models.Model):
        """Log webhook attempts"""
        STATUS_CHOICES = [
            ('pending', 'Pending'),
            ('success', 'Success'),
            ('failed', 'Failed'),
        ]
        
        event_id = models.CharField(max_length=255)
        event = models.CharField(max_length=100)
        data = models.JSONField()
        status = models.CharField(max_length=20, choices=STATUS_CHOICES)
        error = models.TextField(blank=True)
        attempts = models.IntegerField(default=0)
        last_attempt = models.DateTimeField(null=True)
        created_at = models.DateTimeField(auto_now_add=True)
        max_retries = 3
        retry_delay = 300  # 5 minutes

    def process_webhook_with_retry(payload):
        """Process webhook with automatic retry"""
        event_id = payload.get('id')
        
        log, created = WebhookLog.objects.get_or_create(
            event_id=event_id,
            defaults={
                'event': payload.get('event'),
                'data': payload.get('data', {}),
                'status': 'pending'
            }
        )
        
        if log.attempts >= log.max_retries:
            log.status = 'failed'
            log.save()
            return
        
        try:
            handle_event(payload)
            log.status = 'success'
        except Exception as e:
            log.status = 'pending'
            log.error = str(e)
            log.attempts += 1
            log.last_attempt = timezone.now()
            # Could schedule retry with Celery
        
        log.save()

Webhook Monitoring
------------------

Monitor webhook health and failures:

.. code-block:: python

    from django.core.management.base import BaseCommand
    from django.db.models import Q
    from django.utils import timezone
    from datetime import timedelta
    from .models import WebhookLog

    class Command(BaseCommand):
        """Check webhook health"""
        
        def handle(self, *args, **options):
            now = timezone.now()
            five_minutes_ago = now - timedelta(minutes=5)
            
            # Find failures
            failures = WebhookLog.objects.filter(
                status='failed',
                created_at__gte=five_minutes_ago
            )
            
            if failures.exists():
                print(f"⚠️  {failures.count()} webhook failures in last 5 minutes")
                for log in failures:
                    print(f"  - {log.event}: {log.error}")
            
            # Find stuck pending
            stuck = WebhookLog.objects.filter(
                status='pending',
                attempts__gte=3,
                last_attempt__lt=five_minutes_ago
            )
            
            if stuck.exists():
                print(f"❌ {stuck.count()} stuck webhooks")

Best Practices Summary
----------------------

1. **Always verify signatures** - Never process unverified webhooks
2. **Respond quickly** - Return 200 within 3 seconds
3. **Process idempotently** - Handle duplicate events gracefully
4. **Use async processing** - Don't block webhook responses
5. **Implement retry logic** - Handle temporary failures
6. **Log everything** - Keep audit trail of webhook events
7. **Monitor health** - Track failure rates
8. **Test thoroughly** - Use ngrok for local testing

Testing Webhook Security
------------------------

Test webhook signature verification:

.. code-block:: python

    from django.test import TestCase, Client
    from django.conf import settings
    import hmac
    import hashlib
    import json

    class WebhookSecurityTestCase(TestCase):
        
        def test_invalid_signature_rejected(self):
            """Test that invalid signatures are rejected"""
            client = Client()
            
            payload = {
                'event': 'charge.success',
                'data': {'reference': 'test'}
            }
            
            # Send with invalid signature
            response = client.post(
                '/api/webhooks/paystack/',
                data=json.dumps(payload),
                content_type='application/json',
                HTTP_X_PAYSTACK_SIGNATURE='invalid_signature'
            )
            
            self.assertEqual(response.status_code, 401)
        
        def test_valid_signature_accepted(self):
            """Test that valid signatures are accepted"""
            client = Client()
            
            payload = {'event': 'charge.success', 'data': {}}
            webhook_secret = settings.PAYSTACK['WEBHOOK_SECRET']
            
            # Generate valid signature
            signature = hmac.new(
                webhook_secret.encode(),
                json.dumps(payload).encode(),
                hashlib.sha512
            ).hexdigest()
            
            response = client.post(
                '/api/webhooks/paystack/',
                data=json.dumps(payload),
                content_type='application/json',
                HTTP_X_PAYSTACK_SIGNATURE=signature
            )
            
            self.assertEqual(response.status_code, 200)
