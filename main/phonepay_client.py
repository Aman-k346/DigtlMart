# phonepe_client.py

import uuid  
from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest
from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.env import Env
from django.conf import settings

# Initialize the PhonePe client
def get_phonepe_client():
    merchant_id = settings.PHONEPE_MERCHANT_ID
    salt_key = settings.PHONEPE_MERCHANT_KEY
    salt_index = 1
    env = Env.PROD
    should_publish_events = True
    return PhonePePaymentClient(merchant_id, salt_key, salt_index, env, should_publish_events)

def create_payment(amount, user_id):
    phonepe_client = get_phonepe_client()

    # Generate a unique merchantTransactionId (UUID with the last two characters removed)
    unique_transaction_id = str(uuid.uuid4())[:-2]
    ui_redirect_url = "https://2bd7-103-5-134-168.ngrok-free.app/success"
    s2s_callback_url = "https://2bd7-103-5-134-168.ngrok-free.app/callback"

    # Create the payment request
    pay_page_request = PgPayRequest.pay_page_pay_request_builder(
        merchant_transaction_id=unique_transaction_id,  
        amount=amount,
        merchant_user_id=user_id,
        callback_url=s2s_callback_url,
        redirect_url=ui_redirect_url
    )

    pay_page_response = phonepe_client.pay(pay_page_request)
    pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
    merchant_transaction_id = pay_page_response.data.merchant_transaction_id 

    return [pay_page_url, merchant_transaction_id]
