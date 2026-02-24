import requests
import os

# Get credentials from environment variables
api_key = os.environ.get("SENDGRID_API_KEY")
from_email = os.environ.get("SENDGRID_FROM_EMAIL")
to_email = os.environ.get("NOTIFICATION_EMAIL")

# Check if all required variables are set
if not all([api_key, from_email, to_email]):
    print("❌ Error: Missing required environment variables")
    print("\nPlease set the following:")
    if not api_key:
        print("  - SENDGRID_API_KEY")
    if not from_email:
        print("  - SENDGRID_FROM_EMAIL")
    if not to_email:
        print("  - NOTIFICATION_EMAIL")
    print("\nSee instructions above for how to set them.")
    exit(1)

print(f"Testing SendGrid email...")
print(f"From: {from_email}")
print(f"To: {to_email}")
print()

response = requests.post(
    "https://api.sendgrid.com/v3/mail/send",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": from_email},
        "subject": "✓ Test - Mama's Fish House Monitor",
        "content": [{
            "type": "text/plain",
            "value": "SendGrid is working correctly! 🎉\n\nYou're all set to receive email notifications when reservations become available."
        }]
    }
)

print(f"Status Code: {response.status_code}")

if response.status_code == 202:
    print("✅ Success! Email sent.")
    print("\nCheck your inbox (and spam folder) for the test email.")
else:
    print(f"❌ Error: {response.text}")
    print("\nCommon issues:")
    print("  - API key doesn't have 'Mail Send' permission")
    print("  - FROM email isn't verified in SendGrid")
    print("  - API key is incorrect or expired")
