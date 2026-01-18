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
    parser = argparse.ArgumentParser(description="Search Google Contacts")
    parser.add_argument("--query", required=True, help="Name, email, or phone to search for")
    args = parser.parse_args()

    if not TOKEN_FILE.exists():
        print(f"Error: token.json not found. Run auth.py first.", file=sys.stderr)
        return 1

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
    service = build('people', 'v1', credentials=creds)

    try:
        results = service.people().searchContacts(
            query=args.query,
            readMask="names,emailAddresses,phoneNumbers"
        ).execute()

        connections = results.get('results', [])
        if not connections:
            print("No contacts found.")
            return

        formatted_results = []
        for result in connections:
            person = result.get('person', {})
            name = person.get('names', [{}])[0].get('displayName', 'N/A')
            emails = [e.get('value') for e in person.get('emailAddresses', [])]
            phones = [p.get('value') for p in person.get('phoneNumbers', [])]
            
            formatted_results.append({
                "name": name,
                "resourceName": person.get('resourceName'),
                "emails": emails,
                "phones": phones
            })

        print(json.dumps(formatted_results, indent=2))
    except Exception as e:
        print(f"✗ Error searching contacts: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    main()
