from django.conf import settings
import requests


class Paystack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_TEST_SECRET_KEY
    base_url = 'https://api.paystack.co'

    def verify_payment(self, ref, *args, **kwargs):
        path = f'/transaction/verify/{ref}'

        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        url = self.base_url+path
        # url = f"https://api.paystack.co/transaction/verify/{ref}"
        response = requests.get(url, headers=headers)
        print(response)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        response_data = response.json()
        return response_data['status'], response_data['message']
