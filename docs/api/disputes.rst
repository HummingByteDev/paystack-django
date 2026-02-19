.. _api/disputes:

Disputes API
============

Manage transaction disputes raised by customers or their banks.

.. automodule:: djpaystack.api.disputes
   :members:
   :undoc-members:
   :show-inheritance:

Quick Reference
---------------

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

    # List disputes
    client.disputes.list(page=1, per_page=50)

    # Fetch a dispute
    client.disputes.fetch(id='123')

    # List transaction disputes
    client.disputes.list_transaction_disputes(id='txn-123')

    # Update a dispute
    client.disputes.update(id='123', refund_amount=50000)

    # Add evidence
    client.disputes.add_evidence(
        id='123',
        customer_email='customer@example.com',
        customer_name='John Doe',
        customer_phone='2348012345678',
        service_details='Order delivered on 2025-01-15',
    )

    # Get upload URL for evidence files
    client.disputes.get_upload_url(id='123')

    # Resolve a dispute
    client.disputes.resolve(
        id='123',
        resolution='merchant',
        message='Refund issued',
        refund_amount=50000,
    )

    # Export disputes
    client.disputes.export(from_='2025-01-01', to='2025-06-30')

Webhook Events
--------------

- ``charge.dispute.create`` — New dispute raised
- ``charge.dispute.remind`` — Dispute deadline reminder
- ``charge.dispute.resolve`` — Dispute resolved
