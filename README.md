# URL Attribute Monitor

A lightweight monitoring system that periodically checks a URL for specific JSON attributes and sends email notifications when found.

## Features

- Fetches URL and parses JSON response
- Supports nested attribute checking with dot notation (e.g., `data.status.ready`)
- Returns clear exit codes for pipeline integration
- Sends email notifications via SendGrid when attributes are found
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

### 2. Set Up SendGrid

1. Sign up for [SendGrid](https://sendgrid.com/) (free tier: 100 emails/day)
2. Create an API key:
   - Go to Settings > API Keys
   - Click "Create API Key"
   - Choose "Restricted Access" and enable "Mail Send"
   - Copy the API key (you won't see it again!)

### 3. Configure GitHub Secrets

Add these secrets to your GitHub repository (Settings > Secrets and variables > Actions):

- `SENDGRID_API_KEY`: Your SendGrid API key
- `SENDGRID_FROM_EMAIL`: Email address to send from (must be verified in SendGrid)
- `NOTIFICATION_EMAIL`: Email address to receive notifications

### 4. Push to GitHub

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

### Testing SendGrid locally

```python
import requests

response = requests.post(
    "https://api.sendgrid.com/v3/mail/send",
    headers={
        "Authorization": f"Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    json={
        "personalizations": [{"to": [{"email": "your@email.com"}]}],
        "from": {"email": "verified@yourdomain.com"},
        "subject": "Test",
        "content": [{"type": "text/plain", "value": "Test email"}]
    }
)
print(response.status_code, response.text)
```

## Cost

- GitHub Actions: Free (sufficient for this use case)
- SendGrid: Free tier (100 emails/day)
- **Total: $0/month**

## License

MIT
