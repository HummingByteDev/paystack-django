.. _advanced/webhooks:

=========================
Advanced Webhook Handling
=========================

Beyond basic webhook setup, here are advanced patterns and best practices.

How Signature Verification Works
================================

paystack-django automatically verifies every incoming webhook using
``PAYSTACK['SECRET_KEY']`` — the same secret key used for API calls.
You do **not** need a separate webhook secret.

The built-in view (``djpaystack.webhooks.views.PaystackWebhookView``) already
calls ``verify_signature()`` before dispatching events. If you write a custom
view, call it explicitly:

.. code-block:: python

    from djpaystack.webhooks.handlers import PaystackWebhookHandler

    handler = PaystackWebhookHandler()
    if not handler.verify_signature(request):
        return JsonResponse({'error': 'Invalid signature'}, status=401)

See :ref:`advanced/webhook_security` for the full explanation of the HMAC
SHA-512 flow.

Idempotent Processing
=====================

Paystack may re-deliver the same event. Use the built-in
``PaystackWebhookLog`` model (or your own) to deduplicate:

.. code-block:: python

    from djpaystack.models import PaystackWebhookLog

    def process_idempotently(payload):
        event_id = payload.get('id', '')
        log, created = PaystackWebhookLog.objects.get_or_create(
            event_id=event_id,
            defaults={
                'event_type': payload.get('event', ''),
                'payload': payload,
            },
        )
        if not created:
            return  # already processed

        handle_event(payload)
        log.processed = True
        log.save()

Async Processing with Celery
=============================

Return ``200 OK`` immediately and process in the background:

.. code-block:: python

    from celery import shared_task
    from django.http import JsonResponse
    from django.views.decorators.http import require_POST
    import json

    @shared_task
    def process_webhook_async(event, data):
        if event == 'charge.success':
            handle_charge_success(data)
        elif event == 'transfer.success':
            handle_transfer_success(data)

    @require_POST
    def webhook_async(request):
        payload = json.loads(request.body)
        process_webhook_async.delay(
            payload.get('event'),
            payload.get('data'),
        )
        return JsonResponse({'status': 'received'})

Retry Logic
===========

Handle transient failures gracefully:

.. code-block:: python

    from django.utils import timezone

    MAX_RETRIES = 3

    def process_with_retry(log):
        if log.attempts >= MAX_RETRIES:
            log.status = 'failed'
            log.save()
            return

        try:
            handle_event(log.payload)
            log.status = 'success'
        except Exception as exc:
            log.status = 'pending'
            log.error = str(exc)
            log.attempts += 1
            log.last_attempt = timezone.now()
        log.save()

Monitoring Webhook Health
=========================

.. code-block:: python

    from django.core.management.base import BaseCommand
    from django.utils import timezone
    from datetime import timedelta
    from djpaystack.models import PaystackWebhookLog

    class Command(BaseCommand):
        help = 'Check recent webhook health'

        def handle(self, *args, **options):
            since = timezone.now() - timedelta(minutes=30)
            total = PaystackWebhookLog.objects.filter(
                created_at__gte=since,
            ).count()
            failed = PaystackWebhookLog.objects.filter(
                created_at__gte=since, processed=False,
            ).count()
            self.stdout.write(
                f'{total} webhooks in last 30 min — {failed} unprocessed'
            )

Testing Webhook Security
========================

Generate a correctly signed request in your test suite:

.. code-block:: python

    import hmac, hashlib, json
    from django.test import TestCase, Client, override_settings

    SECRET = 'sk_test_xxx'

    @override_settings(PAYSTACK={'SECRET_KEY': SECRET})
    class WebhookSecurityTestCase(TestCase):

        def test_invalid_signature_rejected(self):
            resp = Client().post(
                '/api/webhooks/paystack/',
                data=json.dumps({'event': 'charge.success', 'data': {}}),
                content_type='application/json',
                HTTP_X_PAYSTACK_SIGNATURE='invalid',
            )
            self.assertEqual(resp.status_code, 401)

        def test_valid_signature_accepted(self):
            payload = json.dumps({'event': 'charge.success', 'data': {}})
            sig = hmac.new(
                SECRET.encode(), payload.encode(), hashlib.sha512,
            ).hexdigest()
            resp = Client().post(
                '/api/webhooks/paystack/',
                data=payload,
                content_type='application/json',
                HTTP_X_PAYSTACK_SIGNATURE=sig,
            )
            self.assertEqual(resp.status_code, 200)

Best Practices
==============

1. **Always verify signatures** — never process unverified webhooks.
2. **Respond within 3 seconds** — return ``200`` fast; offload heavy work.
3. **Process idempotently** — handle duplicate deliveries gracefully.
4. **Use async processing** — Celery / Django-Q for long-running handlers.
5. **Implement retry logic** — don't lose events on transient errors.
6. **Log everything** — ``PaystackWebhookLog`` gives you a full audit trail.
7. **Monitor failure rate** — alert when unprocessed webhooks spike.
8. **Test locally** — use ``paystack_listen`` + ``paystack_webhook_event``
   (see :ref:`advanced/local_webhook_testing`).
