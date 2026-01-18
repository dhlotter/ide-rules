#!/usr/bin/env python3
import os
import requests
import argparse
from dotenv import load_dotenv

# Load environment variables from .agent/.env.local relative to this script
# Script is in .agent/skills/beeper-manager/scripts/
# .env.local is in .agent/
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env.local')
load_dotenv(dotenv_path)

# Correct var name from .env.local
TOKEN = os.getenv('BEEPER_DESKTOP_API')
BASE_URL = "http://localhost:23373/v1"

def main():
    parser = argparse.ArgumentParser(description="List Beeper Chats")
    parser.add_argument("--limit", type=int, default=10, help="Number of chats to show")
    parser.add_argument("--search", help="Filter chats by name (case-insensitive)")
    args = parser.parse_args()

    if not TOKEN:
        print("Error: BEEPER_DESKTOP_API not found in .agent/.env.local")
        return

    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    try:
        response = requests.get(f"{BASE_URL}/chats", headers=headers)
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            return

        response_json = response.json()
        chats = response_json.get('items', [])

        print(f"--- Beeper Chats (Top {args.limit}) ---")
        count = 0
        for chat in chats:
            if count >= args.limit:
                break
            
            chat_id = chat.get('id', 'Unknown')
            name = chat.get('title') or chat.get('name') or "Unnamed Chat"
            network = chat.get('network', 'Unknown')
            
            # Simple search filter
            if args.search and args.search.lower() not in name.lower():
                continue

            last_message_obj = chat.get('last_message', {})
            # Sometimes last_message is a dict, sometimes None
            last_msg_body = ""
            if isinstance(last_message_obj, dict):
                last_msg_body = last_message_obj.get('body', '')

            # Clean up newlines for display
            display_msg = last_msg_body.replace('\n', ' ')[:60] + "..." if last_msg_body else ""

            print(f"- [{network}] {name} ({chat_id})")
            if display_msg:
                print(f"  Last: {display_msg}")
            
            count += 1

    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    main()
