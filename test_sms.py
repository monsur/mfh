import os
from twilio.rest import Client

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
from_phone = os.environ.get("TWILIO_FROM_PHONE")
to_phone = os.environ.get("TWILIO_TO_PHONE")

if not all([account_sid, auth_token, from_phone, to_phone]):
    print("Error: Missing required environment variables")
    print("Please set: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_PHONE, TWILIO_TO_PHONE")
    exit(1)

client = Client(account_sid, auth_token)
message = client.messages.create(
    body="Test: Mama's Fish House monitoring is working! 🎉",
    from_=from_phone,
    to=to_phone
)
print(f"SMS sent successfully!")
print(f"Message SID: {message.sid}")
print(f"Status: {message.status}")
