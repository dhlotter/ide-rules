---
name: gmail-inbox-manager
description: Fetches and manages Gmail emails to help reach Inbox Zero.
---

# Gmail Inbox Manager Skill

This skill allows the agent to read your Gmail inbox, summarize emails, and help you organize them into your Obsidian vault.

## Prerequisites

1.  **Google Cloud Project**: A project with the Gmail API enabled.
2.  **Credentials**: A `credentials.json` file placed in `.agent/skills/gmail-inbox-manager/`.
3.  **Authentication**: A valid `token.json` generated via the `auth.py` script.

## Usage

### 1. Authenticate (One-time setup)
Run the authentication script to generate your `token.json`. This will open a browser window for you to log in.
```bash
".agent/skills/gmail-inbox-manager/venv/bin/python" ".agent/skills/gmail-inbox-manager/scripts/auth.py"
```

### 2. Fetch Emails
The agent uses this script to retrieve emails. It can filter by "unread" or specific labels, and limits the number of results to save tokens.
```bash
".agent/skills/gmail-inbox-manager/venv/bin/python" ".agent/skills/gmail-inbox-manager/scripts/fetch_emails.py" --limit 10 --query "is:unread"
```

### 3. Workflow
1.  **Fetch**: The agent runs `fetch_emails.py` to get a JSON list of recent unread emails (Sender, Subject, Snippet/Body).
2.  **Process**: The agent analyzes the emails.
3.  **Action**:
    -   **Summary**: Provide a digest of what's in the inbox.
    -   **File**: Create markdown notes in `00-Inbox` or specific project folders for emails requiring action.
    -   **Draft**: (Future capability) Draft replies or archive emails (requires write scope).

## Setup

1.  Create a virtual environment and install dependencies:
    ```bash
    python3 -m venv ".agent/skills/gmail-inbox-manager/venv"
    source ".agent/skills/gmail-inbox-manager/venv/bin/activate"
    pip install -r ".agent/skills/gmail-inbox-manager/requirements.txt"
    ```
2.  Place your `credentials.json` in this folder.
3.  Run `auth.py` using the virtual environment python.
