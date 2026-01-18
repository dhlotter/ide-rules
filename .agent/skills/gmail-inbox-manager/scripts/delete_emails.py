import argparse
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Updated SCOPES to include modify for deletion
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.send']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')

def get_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("Error: Valid token not found. Please run auth.py first to authenticate.")
            return None

    return build('gmail', 'v1', credentials=creds)

def delete_messages(message_ids):
    service = get_service()
    if not service:
        return

    try:
        if not message_ids:
            print("No message IDs provided for deletion.")
            return

        # Batch delete
        for msg_id in message_ids:
            service.users().messages().trash(userId='me', id=msg_id).execute()
        print(f"Successfully trashed messages with IDs: {', '.join(message_ids)}")

    except Exception as e:
        print(f"An error occurred during message deletion: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Delete Gmail messages.')
    parser.add_argument('message_ids', nargs='+', help='List of message IDs to delete')
    
    args = parser.parse_args()
    delete_messages(args.message_ids)
