
import time
import logging
import subprocess
import requests
from typing import Optional

logger = logging.getLogger('djpaystack.dev')


class NgrokTunnel:
    """
    Manages ngrok tunnel for local webhook development
    Similar to Stripe CLI's webhook forwarding
    """

    def __init__(self, port: int = 8000, region: str = 'us'):
        """
        Initialize ngrok tunnel

        Args:
            port: Local Django server port (default: 8000)
            region: Ngrok region (us, eu, ap, au, sa, jp, in)
        """
        self.port = port
        self.region = region
        self.process: Optional[subprocess.Popen] = None
        self.public_url: Optional[str] = None
        self._check_ngrok_installed()

    def _check_ngrok_installed(self):
        """Check if ngrok is installed"""
        try:
            subprocess.run(
                ['ngrok', 'version'],
                capture_output=True,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "ngrok is not installed. Install it from https://ngrok.com/download\n"
                "On macOS: brew install ngrok\n"
                "On Ubuntu: snap install ngrok\n"
                "On Windows: Download from https://ngrok.com/download"
            )

    def start(self, subdomain: Optional[str] = None, auth_token: Optional[str] = None) -> str:
        """
        Start ngrok tunnel

        Args:
            subdomain: Custom subdomain (requires paid ngrok account)
            auth_token: Ngrok auth token (optional, for features like custom subdomains)

        Returns:
            Public URL of the tunnel
        """
        # Set auth token if provided
        if auth_token:
            subprocess.run(['ngrok', 'config', 'add-authtoken', auth_token])

        # Build ngrok command
        cmd = ['ngrok', 'http', str(self.port), '--region', self.region, '--log', 'stdout']

        if subdomain:
            cmd.extend(['--subdomain', subdomain])

        # Start ngrok process
        logger.info(f"Starting ngrok tunnel on port {self.port}...")
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Wait for tunnel to be ready
        time.sleep(2)

        # Get public URL from ngrok API
        self.public_url = self._get_public_url()

        if self.public_url:
            logger.info(f"✓ Ngrok tunnel started: {self.public_url}")
            logger.info(f"✓ Webhook URL: {self.public_url}/paystack/webhook/")
            return self.public_url
        else:
            raise RuntimeError("Failed to start ngrok tunnel")

    def _get_public_url(self, max_retries: int = 10) -> Optional[str]:
        """Get public URL from ngrok API"""
        for i in range(max_retries):
            try:
                response = requests.get('http://127.0.0.1:4040/api/tunnels')
                if response.status_code == 200:
                    data = response.json()
                    tunnels = data.get('tunnels', [])

                    # Get HTTPS tunnel
                    for tunnel in tunnels:
                        if tunnel.get('proto') == 'https':
                            return tunnel.get('public_url')

                    # Fallback to HTTP
                    if tunnels:
                        return tunnels[0].get('public_url')

            except requests.exceptions.ConnectionError:
                time.sleep(0.5)
                continue

        return None

    def stop(self):
        """Stop ngrok tunnel"""
        if self.process:
            logger.info("Stopping ngrok tunnel...")
            self.process.terminate()
            self.process.wait()
            self.process = None
            self.public_url = None
            logger.info("✓ Ngrok tunnel stopped")

    def get_webhook_url(self) -> str:
        """Get webhook URL"""
        if not self.public_url:
            raise RuntimeError("Ngrok tunnel is not started")
        return f"{self.public_url}/paystack/webhook/"

    def get_dashboard_url(self) -> str:
        """Get ngrok dashboard URL"""
        return "http://127.0.0.1:4040"

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()


def start_ngrok_tunnel(
    port: int = 8000,
    subdomain: Optional[str] = None,
    auth_token: Optional[str] = None,
    region: str = 'us'
) -> NgrokTunnel:
    """
    Convenience function to start ngrok tunnel

    Args:
        port: Local Django server port
        subdomain: Custom subdomain (requires paid plan)
        auth_token: Ngrok auth token
        region: Ngrok region

    Returns:
        NgrokTunnel instance
    """
    tunnel = NgrokTunnel(port=port, region=region)
    tunnel.start(subdomain=subdomain, auth_token=auth_token)
    return tunnel
