#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SKILL_DIR = Path(__file__).parent.parent
TOKEN_FILE = SKILL_DIR / "token.json"

def main():
    parser = argparse.ArgumentParser(description="Delete a Google Contact")
    parser.add_argument("--resource-name", required=True, help="people/c12345")
    args = parser.parse_args()

    if not TOKEN_FILE.exists():
        print(f"Error: token.json not found. Run auth.py first.", file=sys.stderr)
        return 1

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
    service = build('people', 'v1', credentials=creds)

    try:
        service.people().deleteContact(
            resourceName=args.resource_name
        ).execute()
        print(f"✓ Contact deleted successfully: {args.resource_name}")

    except Exception as e:
        print(f"✗ Error deleting contact: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    main()
