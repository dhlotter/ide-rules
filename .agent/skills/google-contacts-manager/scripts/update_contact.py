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
    parser = argparse.ArgumentParser(description="Update a Google Contact")
    parser.add_argument("--resource-name", required=True, help="people/c12345")
    parser.add_argument("--first-name", help="New first name")
    parser.add_argument("--last-name", help="New last name")
    parser.add_argument("--email", help="Add email address")
    parser.add_argument("--phone", help="Add phone number")
    args = parser.parse_args()

    if not TOKEN_FILE.exists():
        print(f"Error: token.json not found. Run auth.py first.", file=sys.stderr)
        return 1

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
    service = build('people', 'v1', credentials=creds)

    try:
        # 1. Fetch current person to get etag and existing fields
        person = service.people().get(
            resourceName=args.resource_name,
            personFields="names,emailAddresses,phoneNumbers"
        ).execute()

        etag = person.get('etag')
        update_mask = []

        if args.first_name or args.last_name:
            names = person.get('names', [{}])
            if not names: names = [{}]
            if args.first_name: names[0]['givenName'] = args.first_name
            if args.last_name: names[0]['familyName'] = args.last_name
            
            # Remove derived/display fields to force regeneration
            names[0].pop('displayName', None)
            names[0].pop('unstructuredName', None)
            
            person['names'] = names
            update_mask.append("names")

        if args.email:
            emails = person.get('emailAddresses', [])
            emails.append({"value": args.email})
            person['emailAddresses'] = emails
            update_mask.append("emailAddresses")

        if args.phone:
            phones = person.get('phoneNumbers', [])
            phones.append({"value": args.phone})
            person['phoneNumbers'] = phones
            update_mask.append("phoneNumbers")

        if not update_mask:
            print("No updates requested.")
            return

        updated_person = service.people().updateContact(
            resourceName=args.resource_name,
            updatePersonFields=",".join(update_mask),
            body=person
        ).execute()

        print(json.dumps(updated_person, indent=2))
        print(f"\n✓ Contact updated successfully: {args.resource_name}")

    except Exception as e:
        print(f"✗ Error updating contact: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    main()
