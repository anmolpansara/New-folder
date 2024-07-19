import json
import os
import secrets

import requests
from django.conf import settings
from django.core.mail import EmailMessage, send_mail

from blogapp.customs.authentications import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            from_email=os.getenv("EMAIL_HOST_USER"),
            to=[data["to_email"]],
        )
        print(email)
        email.send()


def get_tokens_for_user(user):
    # refresh = RefreshToken.for_user(user)
    # access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(
        user.id, user.fcm_token if user.fcm_token else ""
    )
    id, fcm_token = decode_refresh_token(refresh_token)
    refresh_access_token = create_access_token(id, fcm_token)

    return refresh_access_token


# def generate_otp():
#     return secrets.randbelow(900000) + 100000


# def send_otp_twilio(phone_number, body):
#     account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
#     auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
#     client = Client(account_sid, auth_token)
#     print("Sending message to", phone_number, type(phone_number))
#     phone_number_str = str(phone_number)
#     print("Sending message to", phone_number_str, type(phone_number_str))
#     try:
#         message = client.messages.create(
#             from_="+16562253171",
#             body=body,
#             to=phone_number_str,
#         )
#         print("Message sent successfully", message.sid)
#     except Exception as e:
#         print("Error sending message", e)


def generate_otp():
    return str(secrets.randbelow(900000) + 100000)


def send_otp(email, otp):
    subject = "Your OTP Code"
    message = f"Your OTP code is {otp}"
    from_email = "aparsana27@gmail.com"
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def generate_password():
    return str(secrets.randbelow(900000) + 100000)


def send_password(email, password):
    subject = "Your Account Password"
    message = f"Your password is {password}"
    from_email = "aparsana27@gmail.com"
    recipient_list = [email]
    print(recipient_list)
    send_mail(subject, message, from_email, recipient_list)


# def send_password()
# def send_sms_email_gateway(phone_number, otp):
#     gateway_email = "astrospheretalks@yopmail.com"
#     subject = ""
#     message = f"Your OTP for password reset is: {otp}"

#     msg = MIMEText(message)
#     msg["Subject"] = subject
#     msg["From"] = gateway_email
#     msg["To"] = f"{phone_number}@gateway"

#     smtp_server = "localhost"
#     smtp_port = 587
#     smtp_username = "your_email@example.com"
#     smtp_password = "your_email_password"

#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()
#         server.login(smtp_username, smtp_password)
#         server.sendmail(gateway_email, [f"{phone_number}@gateway"], msg.as_string())


# def send_otp(to_email, otp):
#     send_sms_email_gateway("1234567890", "123456")
#     # subject = 'Forgot Password - OTP Verification'
#     # message = f'Your OTP for password reset is: {otp}'
#     # from_email = 'your@example.com'  # Update with your email
#     # send_mail(subject, message, from_email, [to_email])


def capitalize_key(key):
    parts = key.split("_")
    capitalized_parts = [part.capitalize() for part in parts]
    return " ".join(capitalized_parts)


# def currency_conversion(from_currency, to_currency, amount):
#     url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
#     response = requests.get(url)
#     data = response.json()
#     conversion_rate = data["rates"][to_currency]
#     return amount * conversion_rate


def create_razorpay_contact(data):
    razorpay_contact_create_url = "https://api.razorpay.com/v1/contacts"
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(
        razorpay_contact_create_url,
        headers=headers,
        data=json.dumps(data),
        auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET),
        timeout=10,
    )
    print(response.json(), "---------------------")
    return response


def update_razorpay_contact(contact_id, data):
    razorpay_contact_update_url = f"https://api.razorpay.com/v1/contacts/{contact_id}"
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.patch(
        razorpay_contact_update_url,
        headers=headers,
        data=json.dumps(data),
        auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET),
        timeout=10,
    )
    return response


def create_razorpay_fund_account(data):
    razorpay_fund_account_create_url = "https://api.razorpay.com/v1/fund_accounts"
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(
        razorpay_fund_account_create_url,
        headers=headers,
        data=json.dumps(data),
        auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET),
        timeout=10,
    )
    return response


def update_razorpay_fund_account(fund_account_id, data):
    razorpay_fund_account_update_url = (
        f"https://api.razorpay.com/v1/fund_accounts/{fund_account_id}"
    )
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.patch(
        razorpay_fund_account_update_url,
        headers=headers,
        data=json.dumps(data),
        auth=(
            settings.RAZORPAY_API_KEY,
            settings.RAZORPAY_API_SECRET,
        ),
        timeout=10,
    )
    return response


def payout_to_bank_account(data):
    print(data)
    razorpay_payout_url = "https://api.razorpay.com/v1/payouts"
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(
        razorpay_payout_url,
        headers=headers,
        data=json.dumps(data),
        auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET),
        timeout=10,
    )
    return response
