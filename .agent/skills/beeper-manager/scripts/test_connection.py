import requests
import json

URL = "http://localhost:23373/v0/chats"

try:
    response = requests.get(URL)
    if response.status_code == 200:
        chats = response.json()
        print(f"Successfully fetched {len(chats)} chats.")
        # Print first few chats for verification
        for chat in chats[:5]:
            print(f"- {chat.get('name', 'Unknown')}: {chat.get('id')}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Connection failed: {e}")
