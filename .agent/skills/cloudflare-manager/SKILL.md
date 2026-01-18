---
name: cloudflare-manager
description: Manage Cloudflare Pages, DNS, Registrar, and Security directly from your IDE.
---

# Cloudflare Manager Skill

This skill allows you to interact with Cloudflare's platform to monitor Pages deployments, manage DNS records, view security insights, and check domain status without leaving your IDE.

## Features

- ✅ **Pages Monitoring**: List projects, view deployment history, and tail live logs.
- ✅ **DNS Management**: List and query DNS records for your zones.
- ✅ **Domain Insights**: Check registrar status and upcoming renewals.
- ✅ **Security Insights**: Read account-level security risks and recommendations.
- ✅ **Speed Observatory**: Monitor performance metrics (LCP, FID, CLS, Performance Score).
- ✅ **Security & Analytics**: View traffic summaries and security event snapshots.

## Prerequisites

1.  **Cloudflare CLI (`wrangler`)**: Installed and authenticated (`npx wrangler login`).
2.  **API Credentials**:
    - `CLOUDFLARE_API_TOKEN`: Used for direct API calls.
    - `CLOUDFLARE_ACCOUNT_ID`: Your Cloudflare Account ID.

### Required Token Permissions
To use all features, ensure your API Token has:
- `Account` | `Cloudflare Pages` | `Edit`
- `Account` | `Account Analytics` | `Read`
- `Account` | `Security Center` | `Read` (New)
- `Zone` | `DNS` | `Edit`
- `Zone` | `Zone` | `Read`
- `Zone` | `Analytics` | `Read` (New)
- `Zone` | `Speed` | `Read` (New)

## Setup Instructions

### 1. Configure Environment

Create a `.env` file in `.agent/skills/cloudflare-manager/` (or use shell exports):

```bash
CLOUDFLARE_API_TOKEN=your_api_token
CLOUDFLARE_ACCOUNT_ID=your_account_id
```

### 2. Install Python Dependencies (for API-specific tools)

```bash
python3 -m venv ".agent/skills/cloudflare-manager/venv"
source ".agent/skills/cloudflare-manager/venv/bin/activate"
pip install requests python-dotenv
```

## Usage

### Pages Management

#### List Projects
Get a summary of all Pages projects:
```bash
wrangler pages project list
```

#### View Recent Deployments
Check the status of the last few deployments for a specific project:
```bash
wrangler pages deployment list --project-name <project-name>
```

#### Tail Live Logs
Stream logs for the latest deployment of a project:
```bash
wrangler pages deployment tail --project-name <project-name>
```

### DNS & Analytics (via Custom Scripts)

#### List DNS Records
```bash
".agent/skills/cloudflare-manager/venv/bin/python" \
  ".agent/skills/cloudflare-manager/scripts/dns_list.py" --zone-name easyentropy.io
```

#### Get Analytics Summary
```bash
".agent/skills/cloudflare-manager/venv/bin/python" \
  ".agent/skills/cloudflare-manager/scripts/analytics.py" --domain easyentropy.io
```

## Workflows

- **Post-Commit Check**: After pushing code, run `wrangler pages deployment list` to ensure the build started/finished successfully.
- **Log Debugging**: If a build fails or a site is down, use `wrangler pages deployment tail` to see server-side errors in real-time.

## Security

- Never commit your `.env` file or API tokens.
- Tokens should be scoped to "Edit" permissions for specific zones if possible.
