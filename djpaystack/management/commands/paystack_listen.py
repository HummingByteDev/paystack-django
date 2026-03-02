"""
Management command to start a Cloudflare Quick Tunnel for local webhook development.

Usage:
    python manage.py paystack_listen
    python manage.py paystack_listen --host 127.0.0.1 --port 8080
    python manage.py paystack_listen --webhook-path /api/webhooks/paystack/
"""

import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import threading
from typing import Optional

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        "Start a Cloudflare Quick Tunnel to expose your local Django server "
        "for Paystack webhook development."
    )

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--host",
            type=str,
            default="localhost",
            help="Local server hostname (default: localhost)",
        )
        parser.add_argument(
            "--port",
            type=int,
            default=8000,
            help="Local server port (default: 8000)",
        )
        parser.add_argument(
            "--webhook-path",
            type=str,
            default="/webhooks/paystack/",
            help="Webhook URL path (default: /webhooks/paystack/)",
        )

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def handle(self, *args, **options) -> None:
        host: str = options["host"]
        port: int = options["port"]
        webhook_path: str = options["webhook_path"]

        if not self._check_cloudflared():
            return

        local_url = f"http://{host}:{port}"
        self.stdout.write(
            self.style.SUCCESS(
                f"\nStarting Cloudflare Tunnel → {local_url}"
            )
        )

        self._run_tunnel(local_url, webhook_path)

    # ------------------------------------------------------------------
    # Pre-flight: is cloudflared installed?
    # ------------------------------------------------------------------

    def _check_cloudflared(self) -> bool:
        """Return True if cloudflared is available on PATH."""
        if shutil.which("cloudflared"):
            return True

        self.stderr.write(
            self.style.ERROR(
                "\ncloudflared is not installed or not on your PATH.\n"
            )
        )
        self._print_install_instructions()
        return False

    def _print_install_instructions(self) -> None:
        system = platform.system()
        self.stdout.write(self.style.WARNING("Installation instructions:\n"))

        if system == "Linux":
            self.stdout.write("  Debian / Ubuntu:")
            self.stdout.write(
                "    wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb"
                " && sudo dpkg -i cloudflared-linux-amd64.deb\n"
            )
            self.stdout.write("  RHEL / CentOS / Fedora:")
            self.stdout.write(
                "    sudo rpm -i https://pkg.cloudflare.com/cloudflared-linux-x86_64.rpm\n"
            )
            self.stdout.write("  Or download the binary directly:")
            self.stdout.write(
                "    curl -L https://github.com/cloudflare/cloudflared/releases/"
                "latest/download/cloudflared-linux-amd64 -o cloudflared"
            )
            self.stdout.write("    chmod +x cloudflared")
            self.stdout.write("    sudo mv cloudflared /usr/local/bin/\n")

        elif system == "Darwin":
            self.stdout.write("  Homebrew:")
            self.stdout.write("    brew install cloudflared\n")

        elif system == "Windows":
            self.stdout.write("  Winget:")
            self.stdout.write("    winget install Cloudflare.cloudflared\n")
            self.stdout.write("  Or download the installer from:")
            self.stdout.write(
                "    https://github.com/cloudflare/cloudflared/releases/latest\n"
            )
        else:
            self.stdout.write(
                f"  Visit https://developers.cloudflare.com/cloudflare-one/"
                f"connections/connect-networks/downloads/ for {system}.\n"
            )

    # ------------------------------------------------------------------
    # Tunnel lifecycle
    # ------------------------------------------------------------------

    def _run_tunnel(self, local_url: str, webhook_path: str) -> None:
        """Launch cloudflared, extract the public URL, and stream output."""
        cmd = ["cloudflared", "tunnel", "--url", local_url]

        process: Optional[subprocess.Popen] = None

        # Store reference so the signal handler can reach it
        tunnel_url_event = threading.Event()
        tunnel_url_holder: list = []  # mutable container for the URL

        def _on_signal(signum, frame):  # noqa: ANN001
            if process and process.poll() is None:
                process.terminate()
            sys.exit(0)

        signal.signal(signal.SIGINT, _on_signal)
        signal.signal(signal.SIGTERM, _on_signal)

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            url_pattern = re.compile(
                r"(https://[a-zA-Z0-9\-]+\.trycloudflare\.com)"
            )

            for line in iter(process.stdout.readline, ""):
                line = line.rstrip()

                # Try to capture the tunnel URL
                match = url_pattern.search(line)
                if match and not tunnel_url_event.is_set():
                    public_url = match.group(1)
                    tunnel_url_holder.append(public_url)
                    tunnel_url_event.set()
                    self._print_banner(public_url, webhook_path)

                # Forward cloudflared output at DEBUG level
                if line:
                    self.stderr.write(f"  [cloudflared] {line}")

            process.wait()

            if not tunnel_url_event.is_set():
                raise CommandError(
                    "Failed to extract tunnel URL from cloudflared output."
                )

        except FileNotFoundError:
            raise CommandError("cloudflared binary not found.")
        finally:
            if process and process.poll() is None:
                process.terminate()
                process.wait(timeout=5)
            self.stdout.write(self.style.SUCCESS("\nTunnel stopped."))

    # ------------------------------------------------------------------
    # Output helpers
    # ------------------------------------------------------------------

    def _print_banner(self, public_url: str, webhook_path: str) -> None:
        webhook_url = f"{public_url}{webhook_path}"
        sep = "━" * 70

        self.stdout.write(self.style.SUCCESS(f"\n{sep}"))
        self.stdout.write(self.style.SUCCESS(f"  Tunnel URL:   {public_url}"))
        self.stdout.write(self.style.SUCCESS(f"  Webhook URL:  {webhook_url}"))
        self.stdout.write(self.style.SUCCESS(f"{sep}\n"))

        self.stdout.write(self.style.WARNING("  Next steps:\n"))
        self.stdout.write(
            "  1. Make sure your Django server is running:\n"
            f"       python manage.py runserver\n"
        )
        self.stdout.write(
            "  2. Add this webhook URL to your Paystack Dashboard:\n"
            f"       {webhook_url}\n"
            "     https://dashboard.paystack.com/settings/developer\n"
        )
        self.stdout.write(
            "  3. Webhook signature verification uses your\n"
            "     PAYSTACK['SECRET_KEY'] automatically — no extra\n"
            "     configuration required.\n"
        )
        self.stdout.write("  Press Ctrl+C to stop the tunnel.\n")
