.. _advanced/cloudflare_tunnel:

===========================================
Cloudflare Tunnel for Local Development
===========================================

`Cloudflare Quick Tunnels <https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/>`_
expose your local Django server to the internet — perfect for receiving
Paystack webhooks during development. No account or login required.

paystack-django provides a built-in management command that wraps ``cloudflared``
and prints the webhook URL you need to paste into your Paystack Dashboard.

Installing cloudflared
======================

Linux
-----

**Debian / Ubuntu (amd64):**

.. code-block:: bash

   wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
   sudo dpkg -i cloudflared-linux-amd64.deb

**RHEL / CentOS / Fedora:**

.. code-block:: bash

   sudo rpm -i \
       https://pkg.cloudflare.com/cloudflared-linux-x86_64.rpm

**Manual binary (any distro):**

.. code-block:: bash

   curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
       -o cloudflared
   chmod +x cloudflared
   sudo mv cloudflared /usr/local/bin/

macOS
-----

.. code-block:: bash

   brew install cloudflared

Windows
-------

**Winget:**

.. code-block:: powershell

   winget install Cloudflare.cloudflared

**Manual:** Download the latest ``.msi`` from
`GitHub Releases <https://github.com/cloudflare/cloudflared/releases/latest>`_.

Verify the install:

.. code-block:: bash

   cloudflared --version

Quick Tunnel (Manual)
=====================

You can always start a tunnel manually:

.. code-block:: bash

   cloudflared tunnel --url http://localhost:8000

``cloudflared`` prints output like:

.. code-block:: text

   2026-02-21T12:00:00Z INF +----------------------------+
   2026-02-21T12:00:00Z INF |  Your quick Tunnel has been created! ...
   2026-02-21T12:00:00Z INF +----------------------------+
   2026-02-21T12:00:00Z INF https://random-slug-here.trycloudflare.com

Copy the ``https://....trycloudflare.com`` URL, append your webhook path,
and paste it in the
`Paystack Dashboard → Settings → API Keys & Webhooks <https://dashboard.paystack.com/settings/developer>`_:

.. code-block:: text

   https://random-slug-here.trycloudflare.com/webhooks/paystack/

Using ``paystack_listen``
=========================

The built-in management command automates all of the above:

.. code-block:: bash

   python manage.py paystack_listen

This will:

1. Check that ``cloudflared`` is installed (prints install instructions if not).
2. Start a Cloudflare Quick Tunnel pointing at ``http://localhost:8000``.
3. Extract the generated public URL.
4. Print the complete **Webhook URL** ready to paste into the Paystack Dashboard.

Example output:

.. code-block:: text

   Starting Cloudflare Tunnel → http://localhost:8000

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     Tunnel URL:   https://random-slug-here.trycloudflare.com
     Webhook URL:  https://random-slug-here.trycloudflare.com/webhooks/paystack/
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

     Next steps:

     1. Make sure your Django server is running:
          python manage.py runserver

     2. Add this webhook URL to your Paystack Dashboard:
          https://random-slug-here.trycloudflare.com/webhooks/paystack/
        https://dashboard.paystack.com/settings/developer

     3. Webhook signature verification uses your
        PAYSTACK['SECRET_KEY'] automatically — no extra
        configuration required.

     Press Ctrl+C to stop the tunnel.

Command Options
---------------

.. code-block:: text

   --host HOST           Local server hostname (default: localhost)
   --port PORT           Local server port (default: 8000)
   --webhook-path PATH   Webhook URL path (default: /webhooks/paystack/)

Examples:

.. code-block:: bash

   # Custom port
   python manage.py paystack_listen --port 8080

   # Custom host and webhook path
   python manage.py paystack_listen --host 0.0.0.0 --port 9000 \
       --webhook-path /api/v1/webhooks/paystack/

Stopping the Tunnel
-------------------

Press **Ctrl+C** in the terminal. The command catches the interrupt signal
and cleanly terminates the ``cloudflared`` process.

Troubleshooting
===============

**"cloudflared is not installed"**
   Run the install command for your OS (see above) and make sure ``cloudflared``
   is on your ``PATH``.

**Tunnel starts but Django returns 403 / 400**
   - Check that your Django server is actually running (``python manage.py runserver``).
   - If you have IP whitelisting enabled (``PAYSTACK['ALLOWED_WEBHOOK_IPS']``),
     you may need to add the Cloudflare egress IPs or clear the list during
     local development.
   - Ensure ``PAYSTACK['SECRET_KEY']`` matches the key shown in your
     Paystack Dashboard.

**"Connection refused"**
   The tunnel URL is correct but Django isn't listening on the expected
   host/port. Make sure ``--port`` matches the port you passed to ``runserver``.

.. note::

   Cloudflare Quick Tunnels are ephemeral — the URL changes every time you
   restart the command. This is by design for development use. Do **not** use
   Quick Tunnels in production.
