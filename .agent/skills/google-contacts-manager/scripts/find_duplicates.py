#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path
from collections import defaultdict
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SKILL_DIR = Path(__file__).parent.parent
TOKEN_FILE = SKILL_DIR / "token.json"

def normalize_phone(phone):
    """Simple normalization: remove spaces, dashes, parentheses."""
    if not phone:
        return ""
    return "".join(filter(str.isdigit, phone))

def main():
    if not TOKEN_FILE.exists():
        print(f"Error: token.json not found. Run auth.py first.", file=sys.stderr)
        return 1

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
    service = build('people', 'v1', credentials=creds)

    print("Fetching contacts...", file=sys.stderr)
    
    connections_list = []
    page_token = None
    
    try:
        while True:
            results = service.people().connections().list(
                resourceName='people/me',
                pageSize=1000,
                personFields='names,phoneNumbers',
                pageToken=page_token
            ).execute()
            
            connections = results.get('connections', [])
            connections_list.extend(connections)
            
            page_token = results.get('nextPageToken')
            if not page_token:
                break

    except Exception as e:
        print(f"✗ Error fetching contacts: {e}", file=sys.stderr)
        return 1

    print(f"Analyzed {len(connections_list)} contacts.", file=sys.stderr)

    phone_map = defaultdict(list)
    name_map = defaultdict(list)
    empty_contacts = []
    
    for person in connections_list:
        resource_name = person.get('resourceName')
        names = person.get('names', [])
        display_name = names[0].get('displayName', 'No Name') if names else 'No Name'
        
        phone_numbers = person.get('phoneNumbers', [])
        emails = person.get('emailAddresses', [])

        # Check for empty contacts
        if not phone_numbers and not emails:
            empty_contacts.append({"name": display_name, "id": resource_name})

        # Map by Name
        if display_name and display_name != 'No Name':
            name_map[display_name.lower().strip()].append({
                "name": display_name,
                "id": resource_name,
                "info": f"{len(phone_numbers)} phones, {len(emails)} emails"
            })
        
        # Map by Phone
        for phone in phone_numbers:
            original_value = phone.get('value')
            norm_key = normalize_phone(original_value)
            
            if norm_key:
                phone_map[norm_key].append({
                    "name": display_name,
                    "id": resource_name,
                    "phone_display": original_value
                })

    # Report Phone Duplicates
    phone_duplicates = {k: v for k, v in phone_map.items() if len(v) > 1}
    # Filter out same-contact duplicates (same ID)
    clean_phone_dupes = {}
    for k, v in phone_duplicates.items():
        unique_ids = set(c['id'] for c in v)
        if len(unique_ids) > 1:
            clean_phone_dupes[k] = v

    # Report Name Duplicates
    name_duplicates = {k: v for k, v in name_map.items() if len(v) > 1}

    print("\n--- 🔍 Contact Audit Report ---\n")

    if empty_contacts:
        print(f"👻 FOUND {len(empty_contacts)} GHOST CONTACTS (No Phone/Email):")
        for c in empty_contacts[:10]: # Limit output
            print(f"  - {c['name']} [{c['id']}]")
        if len(empty_contacts) > 10: print(f"  ... and {len(empty_contacts)-10} more.")
        print("-" * 40)

    if name_duplicates:
        print(f"\n👯 FOUND {len(name_duplicates)} DUPLICATE NAMES:")
        for name, contacts in name_duplicates.items():
            print(f"Name: '{contacts[0]['name']}'")
            for c in contacts:
                print(f"  - {c['info']} [{c['id']}]")
            print("-" * 40)

    if clean_phone_dupes:
        print(f"\n📞 FOUND {len(clean_phone_dupes)} PHONE DUPLICATES:")
        for phone, contacts in clean_phone_dupes.items():
            print(f"Phone: {phone}")
            for c in contacts:
                print(f"  - {c['name']} ({c['phone_display']}) [{c['id']}]")
            print("-" * 40)
            
    if not empty_contacts and not name_duplicates and not clean_phone_dupes:
        print("✅ No issues found! Your contact list is squeaky clean.")

if __name__ == "__main__":
    main()
