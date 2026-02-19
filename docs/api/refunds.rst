.. _api/refunds:

Refunds API
===========

.. automodule:: djpaystack.api.refunds
   :members:
   :undoc-members:
   :show-inheritance:

Quick Reference
---------------

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

    # Create refund
    client.refunds.create(transaction='123456', amount=50000)

    # List refunds
    client.refunds.list(page=1, per_page=50)

    # Fetch refund
    client.refunds.fetch(reference='refund-ref')

    # Retry a stuck refund (status = refund.needs-attention)
    client.refunds.retry(id='123456')

Webhook Events
--------------

- ``refund.pending`` — Refund initiated
- ``refund.processing`` — Refund in progress
- ``refund.processed`` — Refund completed
- ``refund.failed`` — Refund failed
- ``refund.needs-attention`` — Requires manual retry via ``retry()``
