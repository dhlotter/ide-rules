---
name: beeper-manager
description: Manage and interact with Beeper Desktop (WhatsApp, iMessage, etc.) from the terminal.
---

# Beeper Manager Skill

This skill integrates with the Beeper Desktop local API to read chats, list messages, and search conversations across all your connected networks (WhatsApp, Telegram, iMessage, etc.).

## Prerequisites

1.  **Beeper Desktop**: Must be installed and running.
2.  **API Enabled**: Settings -> Developers -> Enable Beeper Desktop API.
3.  **API Token**: Created in Settings -> Developers -> Approved connections.

## Features

- ✅ List recent active chats.
- ✅ Read message history from a specific chat.
- ✅ Search for messages across conversations.
- ✅ Send messages (optional/advanced).

## Setup

1.  Install dependencies:
    ```bash
    python3 -m venv ".agent/skills/beeper-manager/venv"
    source ".agent/skills/beeper-manager/venv/bin/activate"
    pip install requests python-dotenv
    ```

2.  Configure `.env`:
    ```bash
    echo "BEEPER_TOKEN=your-token-here" > ".agent/skills/beeper-manager/.env"
    ```

## Usage

### List Chats
```bash
".agent/skills/beeper-manager/venv/bin/python" \
  ".agent/skills/beeper-manager/scripts/list_chats.py" --limit 10
```

### Read Messages
```bash
".agent/skills/beeper-manager/venv/bin/python" \
  ".agent/skills/beeper-manager/scripts/get_messages.py" --chat-id "chat-xyz"
```
