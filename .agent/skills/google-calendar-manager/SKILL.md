---
name: google-calendar-manager
description: Fetches and manages Google Calendar events.
---

# Google Calendar Manager Skill

This skill allows the agent to read, add, update, and delete Google Calendar events.

## Prerequisites

1.  **Google Cloud Project**: A project with the Google Calendar API enabled.
2.  **Credentials**: A `credentials.json` file placed in `.agent/skills/google-calendar-manager/`.
3.  **Authentication**: A valid `token.json` generated via the `auth.py` script.

## Usage

### 1. Authenticate (One-time setup)
Run the authentication script to generate your `token.json`. This will open a browser window for you to log in.
```bash
".agent/skills/google-calendar-manager/venv/bin/python" ".agent/skills/google-calendar-manager/scripts/auth.py"
```

### 2. Manage Events
The agent uses the `manage_calendar.py` script to interact with your calendar.

#### Add an Event
```bash
".agent/skills/google-calendar-manager/venv/bin/python" ".agent/skills/google-calendar-manager/scripts/manage_calendar.py" add --summary "nymly Launch" --start "2026-02-09T00:00:00Z" --description "https://tinylaunch.com/launch/9350"
```

#### List Events
```bash
".agent/skills/google-calendar-manager/venv/bin/python" ".agent/skills/google-calendar-manager/scripts/manage_calendar.py" list --limit 10
```

#### Update an Event
```bash
".agent/skills/google-calendar-manager/venv/bin/python" ".agent/skills/google-calendar-manager/scripts/manage_calendar.py" update --id "EVENT_ID" --summary "New Title"
```

#### Delete an Event
```bash
".agent/skills/google-calendar-manager/venv/bin/python" ".agent/skills/google-calendar-manager/scripts/manage_calendar.py" delete --id "EVENT_ID"
```

## Setup

1.  Create a virtual environment and install dependencies:
    ```bash
    python3 -m venv ".agent/skills/google-calendar-manager/venv"
    source ".agent/skills/google-calendar-manager/venv/bin/activate"
    pip install -r ".agent/skills/google-calendar-manager/requirements.txt"
    ```
2.  Place your `credentials.json` in this folder (copied from `gmail-inbox-manager`).
3.  Run `auth.py` using the virtual environment python.
