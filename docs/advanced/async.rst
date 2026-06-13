.. _advanced/async:

Async Usage
===========

.. note::

   The Paystack client in paystack-django is **synchronous** (it uses
   ``requests``). A native async client is on the roadmap. In the meantime you
   can safely call the client from async Django views by offloading the blocking
   call with ``asgiref.sync.sync_to_async``.

Calling the client from an async view
-------------------------------------

.. code-block:: python

    from django.http import JsonResponse
    from django.views.decorators.http import require_http_methods
    from asgiref.sync import sync_to_async

    from djpaystack import PaystackClient

    client = PaystackClient()

    @require_http_methods(["POST"])
    async def async_checkout(request):
        """Initialize a payment from an async view."""
        response = await sync_to_async(client.transactions.initialize)(
            email=request.POST["email"],
            amount=int(request.POST["amount"]),
        )
        return JsonResponse(response["data"])

Why ``sync_to_async``?
----------------------

Calling a blocking HTTP client directly inside an async view would block the
event loop. ``sync_to_async`` runs the call in a thread pool so the loop stays
responsive. This is the recommended pattern until a native async client ships.

Roadmap
-------

A native ``AsyncPaystackClient`` (built on ``httpx``) is planned for a future
major release. Until then, the ``sync_to_async`` pattern above is the supported
way to use paystack-django in async contexts.
