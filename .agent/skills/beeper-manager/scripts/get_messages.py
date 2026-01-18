#!/usr/bin/env python3
import os
import requests
import argparse
from dotenv import load_dotenv

# Load global env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env.local')
load_dotenv(dotenv_path)

TOKEN = os.getenv('BEEPER_DESKTOP_API')
BASE_URL = "http://localhost:23373/v1"

def main():
    parser = argparse.ArgumentParser(description="Get messages from a Beeper Chat")
    parser.add_argument("--chat-id", required=True, help="The ID of the chat to read")
    parser.add_argument("--limit", type=int, default=10, help="Number of messages to retrieve")
    args = parser.parse_args()

    if not TOKEN:
        print("Error: BEEPER_DESKTOP_API not found in .agent/.env.local")
        return

    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    try:
        # Beeper API endpoint for messages in a chat
        url = f"{BASE_URL}/chats/{args.chat_id}/messages?limit={args.limit}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            return

        result = response.json()
        messages = result.get('messages', [])

        print(f"--- Messages for Chat {args.chat_id} ---")
        # Messages usually come latest first or last first, let's reverse to show conversation flow if needed
        # Assuming reverse chronological (newest first) from API, so reverse for display
        for msg in reversed(messages):
            sender = msg.get('sender_id', 'Unknown')
            body = msg.get('body', '')
            timestamp = msg.get('created_at', '')
            
            # Simple cleanup
            if not body:
                body = "<Media/System Message>"
            
            print(f"[{sender[-10:]}] {body}")

    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    main()
