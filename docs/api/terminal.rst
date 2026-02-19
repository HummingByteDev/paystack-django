.. _api/terminal:

Terminal & Apple Pay API
========================

Terminal
--------

.. automodule:: djpaystack.api.terminal
   :members:
   :undoc-members:
   :show-inheritance:

Virtual Terminal
----------------

.. automodule:: djpaystack.api.virtual_terminal
   :members:
   :undoc-members:
   :show-inheritance:

Apple Pay
---------

.. automodule:: djpaystack.api.apple_pay
   :members:
   :undoc-members:
   :show-inheritance:

Quick Reference
---------------

.. code-block:: python

    from djpaystack import PaystackClient
    client = PaystackClient()

    # Terminal
    client.terminal.send_event(terminal_id=..., type=..., action=..., data=...)
    client.terminal.fetch_event_status(terminal_id=..., event_id=...)
    client.terminal.fetch_terminal_status(terminal_id=...)
    client.terminal.list()
    client.terminal.fetch(terminal_id=...)
    client.terminal.update(terminal_id=..., name=..., address=...)
    client.terminal.commission(serial_number=...)
    client.terminal.decommission(serial_id=...)

    # Apple Pay
    client.apple_pay.register(domain_name='example.com')
    client.apple_pay.list()
    client.apple_pay.unregister(domain_name='example.com')
