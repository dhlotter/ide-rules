#!/usr/bin/env python3
import os
import sys
import argparse
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SKILL_DIR = Path(__file__).parent.parent
TOKEN_FILE = SKILL_DIR / "token.json"

def main():
    parser = argparse.ArgumentParser(description="Create a Google Contact")
    parser.add_argument("--first-name", required=True)
    parser.add_argument("--last-name", default="")
    parser.add_argument("--email", help="Email address")
    parser.add_argument("--phone", help="Phone number")
    args = parser.parse_args()

    if not TOKEN_FILE.exists():
        print(f"Error: token.json not found. Run auth.py first.", file=sys.stderr)
        return 1

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
    service = build('people', 'v1', credentials=creds)

    body = {
        "names": [{"givenName": args.first_name, "familyName": args.last_name}],
    }

    if args.email:
        body["emailAddresses"] = [{"value": args.email}]
    if args.phone:
        body["phoneNumbers"] = [{"value": args.phone}]

    try:
        contact = service.people().createContact(body=body).execute()
        print(json.dumps(contact, indent=2))
        print(f"\n✓ Contact created successfully: {contact.get('resourceName')}")
    except Exception as e:
        print(f"✗ Error creating contact: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    main()
