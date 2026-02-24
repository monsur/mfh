# Mama's Fish House Reservation Monitor

A lightweight monitoring system that checks Mama's Fish House restaurant for reservation availability and sends **both email and SMS notifications** when slots become available.

## Features

- Fetches SevenRooms API and parses JSON response for bookable reservations
- Checks for `"type": "book"` in availability times array
- Returns clear exit codes for pipeline integration
- Sends **dual notifications** when availability is found:
  - **Email** via SendGrid (free, detailed info with links)
  - **SMS** via Twilio (immediate alert, hard to miss)
- Runs automatically every 15 minutes via GitHub Actions

## Setup

### 1. Configure the URL and Attributes

Edit `config.yaml`:

```yaml
url: "https://your-api.example.com/endpoint"
attributes:
  - "status"
  - "data.ready"
timeout: 10
```

### 2. Set Up SendGrid (Email Notifications)

1. Sign up for [SendGrid](https://sendgrid.com/) (free tier: 100 emails/day)
2. Create an API key:
   - Go to Settings > API Keys
   - Click "Create API Key"
   - Choose "Restricted Access" and enable "Mail Send"
   - Copy the API key (you won't see it again!)
3. Verify your sender email address in SendGrid

### 3. Set Up Twilio (SMS Notifications)

1. Sign up for [Twilio](https://www.twilio.com/try-twilio) (free trial with $15 credit ≈ 1,500 messages)
2. Get a trial phone number (assigned automatically during signup)
3. Find your credentials in the Twilio Console:
   - **Account SID**
   - **Auth Token**
   - **Trial Phone Number** (format: +1234567890)
4. Verify your personal phone number during signup (required for trial)

### 4. Configure GitHub Secrets

Add these secrets to your GitHub repository (Settings > Secrets and variables > Actions):

**SendGrid (Email):**
- `SENDGRID_API_KEY`: Your SendGrid API key
- `SENDGRID_FROM_EMAIL`: Email address to send from (must be verified in SendGrid)
- `NOTIFICATION_EMAIL`: Email address to receive notifications

**Twilio (SMS):**
- `TWILIO_ACCOUNT_SID`: Account SID from Twilio Console
- `TWILIO_AUTH_TOKEN`: Auth Token from Twilio Console
- `TWILIO_FROM_PHONE`: Twilio trial number (e.g., +15558675309)
- `TWILIO_TO_PHONE`: Your personal phone number (e.g., +15551234567)

**Total: 7 GitHub Secrets**

### 5. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

The workflow will start running automatically every 15 minutes.

## Local Testing

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the checker:

```bash
python check_url.py
```

### Exit codes:

- `0` - Success (attribute found)
- `1` - Not found (attribute missing from valid JSON)
- `2` - Error (network error, invalid JSON, timeout, etc.)

### Test with a sample JSON API:

```yaml
# config.yaml
url: "https://httpbin.org/json"
attributes:
  - "slideshow.title"
```

## Manual Workflow Trigger

You can manually trigger the workflow from GitHub:
1. Go to Actions tab
2. Select "URL Attribute Monitor"
3. Click "Run workflow"

## Customization

### Change schedule

Edit `.github/workflows/monitor.yml`:

```yaml
schedule:
  - cron: '0 * * * *'  # Every hour
  - cron: '0 0 * * *'  # Daily at midnight
  - cron: '*/30 * * * *'  # Every 30 minutes
```

### Customize email content

Edit the `text` field in the workflow file to include more details or format differently.

### Check multiple URLs

Create separate config files and workflow files for each URL you want to monitor.

## Troubleshooting

### Workflow not running?

- Check if scheduled workflows are enabled in your repo settings
- Private repos have 2000 free minutes/month; public repos are unlimited
- GitHub may disable workflows if the repo has no activity for 60 days

### Not receiving emails?

- Verify SendGrid API key has "Mail Send" permission
- Check that `SENDGRID_FROM_EMAIL` is verified in SendGrid
- Look for errors in the GitHub Actions logs

### Not receiving SMS?

- Verify all 4 Twilio secrets are correctly set in GitHub
- Check phone numbers are in E.164 format (+1234567890)
- For trial accounts, ensure recipient number is verified in Twilio
- Look for errors in the GitHub Actions logs (SMS step)
- Check Twilio Console → Monitor → Logs for message status

### Testing SMS locally

Create `test_sms.py`:

```python
import os
from twilio.rest import Client

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
from_phone = os.environ.get("TWILIO_FROM_PHONE")
to_phone = os.environ.get("TWILIO_TO_PHONE")

client = Client(account_sid, auth_token)
message = client.messages.create(
    body="Test: Mama's Fish House monitoring is working!",
    from_=from_phone,
    to=to_phone
)
print(f"SMS sent: {message.sid}")
```

Run with:
```bash
export TWILIO_ACCOUNT_SID="your_sid"
export TWILIO_AUTH_TOKEN="your_token"
export TWILIO_FROM_PHONE="+15558675309"
export TWILIO_TO_PHONE="+15551234567"
python test_sms.py
```

## Cost

- **GitHub Actions**: Free (2000 minutes/month for private repos, unlimited for public)
- **SendGrid Email**: Free tier (100 emails/day) - more than sufficient
- **Twilio SMS**:
  - Free trial: $15 credit ≈ 1,500 messages (covers several months of testing)
  - Production: ~$0.01 per SMS sent
  - **Only sends when availability is found** (not every 15-minute check!)
  - Realistic cost: $1-5/month depending on how often reservations appear

**Total: $0-5/month** (free during trial, minimal cost after)

### Why Both Email AND SMS?

- **Email**: Free, includes links, detailed info, permanent record
- **SMS**: Immediate alert, higher visibility, hard to miss
- **Together**: Get instant alert (SMS) + detailed follow-up (email)
- **Cost-effective**: SMS only triggers on success, not every check

### Disable SMS to Save Money

If you want to disable SMS and only use email notifications:
1. Comment out or delete the "Send SMS notification" step in `.github/workflows/monitor.yml`
2. Keep only the email notification step
3. No code changes needed - just edit the workflow file

## License

MIT
