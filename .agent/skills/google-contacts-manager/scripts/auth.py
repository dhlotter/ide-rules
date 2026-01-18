#!/usr/bin/env python3
"""
Authentication script for Google Contacts Manager.
Generates token.json for API access.
"""

import os
import sys
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes required for Google Contacts
SCOPES = ['https://www.googleapis.com/auth/contacts']

SKILL_DIR = Path(__file__).parent.parent
CREDENTIALS_FILE = SKILL_DIR / "credentials.json"
TOKEN_FILE = SKILL_DIR / "token.json"

def main():
    print("=" * 60)
    print("Google Contacts Manager - Authentication")
    print("=" * 60)
    print()
    
    # Check if credentials.json exists
    if not CREDENTIALS_FILE.exists():
        print(f"Error: credentials.json not found at {CREDENTIALS_FILE}", file=sys.stderr)
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
    print("Testing connection to Google People API...")
    try:
        service = build('people', 'v1', credentials=creds)
        results = service.people().getBatchGet(
            resourceNames=['people/me'],
            personFields='names'
        ).execute()
        print("✓ Successfully connected to Google People API!")
    except Exception as e:
        print(f"✗ Error testing connection: {e}", file=sys.stderr)
        return 1
    
    print()
    print("=" * 60)
    print("Authentication complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
