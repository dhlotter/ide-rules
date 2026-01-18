#!/usr/bin/env python3
"""
Authentication script for Google Tasks Manager.
Generates token.json for API access.
"""

import os
import sys
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes required for Google Tasks
SCOPES = ['https://www.googleapis.com/auth/tasks']

SKILL_DIR = Path(__file__).parent.parent
CREDENTIALS_FILE = SKILL_DIR / "credentials.json"
TOKEN_FILE = SKILL_DIR / "token.json"

def main():
    print("=" * 60)
    print("Google Tasks Manager - Authentication")
    print("=" * 60)
    print()
    
    # Check if credentials.json exists
    if not CREDENTIALS_FILE.exists():
        print(f"Error: credentials.json not found at {CREDENTIALS_FILE}", file=sys.stderr)
        print()
        print("Please either:")
        print("1. Copy from existing skill:")
        print('   cp ".agent/skills/gmail-inbox-manager/credentials.json" \\')
        print('      ".agent/skills/google-tasks-manager/credentials.json"')
        print()
        print("2. Or create new credentials at:")
        print("   https://console.cloud.google.com/")
        print("   - Enable Google Tasks API")
        print("   - Create OAuth 2.0 credentials")
        print("   - Download as credentials.json")
        print()
        return 1
    
    creds = None
    
    # Load existing token if available
    if TOKEN_FILE.exists():
        print("Found existing token.json")
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Starting OAuth flow...")
            print("A browser window will open for authentication.")
            print()
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save the credentials
        TOKEN_FILE.write_text(creds.to_json())
        print(f"✓ Token saved to {TOKEN_FILE}")
    else:
        print("✓ Token is valid")
    
    # Test the connection
    print()
    print("Testing connection to Google Tasks API...")
    try:
        service = build('tasks', 'v1', credentials=creds)
        results = service.tasklists().list(maxResults=1).execute()
        print("✓ Successfully connected to Google Tasks API!")
        
        if 'items' in results and len(results['items']) > 0:
            print(f"✓ Found task list: {results['items'][0]['title']}")
    except Exception as e:
        print(f"✗ Error testing connection: {e}", file=sys.stderr)
        return 1
    
    print()
    print("=" * 60)
    print("Authentication complete!")
    print("=" * 60)
    print()
    print("You can now use the Google Tasks Manager skill.")
    print()
    print("Try running:")
    print('  ".agent/skills/google-tasks-manager/venv/bin/python" \\')
    print('    ".agent/skills/google-tasks-manager/scripts/list_task_lists.py"')
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
