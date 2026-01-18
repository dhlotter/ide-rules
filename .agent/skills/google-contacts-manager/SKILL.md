---
name: google-contacts-manager
description: Manage Google Contacts to create, search, and update contacts from your life operating system.
---

# Google Contacts Manager Skill

This skill allows you to interface with the Google People API to create and manage contacts, making it easy to save leads, partners, or friends directly from your IDE.

## Prerequisites

1.  **Google Cloud Project**: A project with the **Google People API** enabled.
2.  **Credentials**: A `credentials.json` file (you can reuse the one from `google-tasks-manager` or `gmail-inbox-manager`).
3.  **Authentication**: A valid `token.json` generated via the `auth.py` script.

## Features

- ✅ Create new contacts with names, emails, and phone numbers.
- ✅ Search for existing contacts by name or email.
- ✅ Update existing contacts with new information.
- ✅ List recent or all contacts.

## Setup Instructions

### 1. Install Dependencies

Create a virtual environment and install required packages:

```bash
python3 -m venv ".agent/skills/google-contacts-manager/venv"
source ".agent/skills/google-contacts-manager/venv/bin/activate"
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 2. Setup Credentials

Re-use your existing Google Cloud credentials:
```bash
cp ".agent/skills/google-tasks-manager/credentials.json" \
   ".agent/skills/google-contacts-manager/credentials.json"
```

### 3. Authenticate

Run the authentication script (opens browser for OAuth):

```bash
".agent/skills/google-contacts-manager/venv/bin/python" \
  ".agent/skills/google-contacts-manager/scripts/auth.py"
```

## Usage

### Create a Contact
```bash
".agent/skills/google-contacts-manager/venv/bin/python" \
  ".agent/skills/google-contacts-manager/scripts/create_contact.py" \
  --first-name "John" --last-name "Doe" \
  --email "john@example.com" --phone "+27123456789"
```

### Search for a Contact
```bash
".agent/skills/google-contacts-manager/venv/bin/python" \
  ".agent/skills/google-contacts-manager/scripts/search_contacts.py" --query "John"
```

### Add Info to Existing Contact
```bash
".agent/skills/google-contacts-manager/venv/bin/python" \
  ".agent/skills/google-contacts-manager/scripts/update_contact.py" \
  --resource-name "people/c12345" --phone "+27987654321"
```

## API Notes
- Uses the **Google People API**.
- Resource names (IDs) are in the format `people/c<id>`.
