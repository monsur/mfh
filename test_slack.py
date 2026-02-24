import os
import requests
import json

webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

if not webhook_url:
    print("Error: Missing SLACK_WEBHOOK_URL environment variable")
    print("Please set it with: export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/YOUR/WEBHOOK/URL'")
    exit(1)

# Build Slack message using Block Kit for rich formatting
message = {
    "text": "🎉 Mamas Fish House - Reservations Available!",
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "🎉 *Mamas Fish House - Reservations Available!*\n\nGreat news! Reservations are available at Mamas Fish House!"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "<https://www.sevenrooms.com/reservations/mamasfishhouserestaurantinn|Book Now>"
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "This is a test notification"
                }
            ]
        }
    ]
}

print(f"Sending test message to Slack...")
response = requests.post(webhook_url, json=message)

if response.status_code == 200:
    print("✅ Slack notification sent successfully!")
    print(f"Response: {response.text}")
else:
    print(f"❌ Failed to send Slack notification")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    exit(1)
