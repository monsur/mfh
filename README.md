# Mama's Fish House Reservation Monitor

A lightweight monitoring system that checks Mama's Fish House restaurant for reservation availability and sends **email and Slack notifications** when slots become available.

## Features

- Fetches SevenRooms API and parses JSON response for bookable reservations
- Checks for `"type": "book"` in availability times array
- Returns clear exit codes for pipeline integration
- Sends **dual notifications** when availability is found:
  - **Email** via SendGrid (free, detailed info)
  - **Slack** via webhook (instant chat notification)
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
3. Verify your sender email address in SendGrid:
   - Go to Settings → Sender Authentication → Verify a Single Sender
   - Enter your email and verify it

### 3. Set Up Slack (Chat Notifications)

1. Go to https://api.slack.com/apps
2. Click **Create New App** → **From scratch**
3. Name it "Mamas Fish House Monitor"
4. Select your workspace (or create a new one at https://slack.com/create)
5. Click **Incoming Webhooks** in the sidebar
6. Toggle **Activate Incoming Webhooks** to ON
7. Click **Add New Webhook to Workspace**
8. Choose a channel (create `#reservations` or use `#general`)
9. Click **Allow**
10. Copy the **Webhook URL** (looks like: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX`)

### 4. Configure GitHub Secrets

Add these secrets to your GitHub repository (Settings > Secrets and variables > Actions):

**SendGrid (Email):**
- `SENDGRID_API_KEY`: Your SendGrid API key
- `SENDGRID_FROM_EMAIL`: Email address to send from (must be verified in SendGrid)
- `NOTIFICATION_EMAIL`: Email address to receive notifications

**Slack (Chat):**
- `SLACK_WEBHOOK_URL`: Your Slack webhook URL

**Total: 4 GitHub Secrets**

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
- Check your spam folder

### Not receiving Slack messages?

- Verify `SLACK_WEBHOOK_URL` is correctly set in GitHub Secrets
- Check the webhook URL is complete and starts with `https://hooks.slack.com/services/`
- Verify the Slack app has permission to post to the channel
- Look for errors in the GitHub Actions logs (Slack notification step)

### Testing Slack locally

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
python test_slack.py
```

### Push notifications

- **Email**: Most email apps send instant push notifications to your phone
- **Slack**: Slack mobile app provides real-time push notifications
- Together, you're covered on all devices!

## Cost

- **GitHub Actions**: Free (2000 minutes/month for private repos, unlimited for public)
- **SendGrid Email**: Free tier (100 emails/day) - more than sufficient
- **Slack**: Free (unlimited messages on free workspace)

**Total: $0/month** ✅

### Why Email + Slack Works Great

**Email Benefits:**
- ✅ Free forever, no limits
- ✅ Detailed info with formatting
- ✅ Searchable history
- ✅ Clickable links

**Slack Benefits:**
- ✅ Free forever, no limits
- ✅ Real-time chat notifications
- ✅ Clean, formatted messages
- ✅ Mobile push notifications
- ✅ Easy to see at a glance

**Together:** Best of both worlds - instant alerts + permanent records!

## License

MIT
