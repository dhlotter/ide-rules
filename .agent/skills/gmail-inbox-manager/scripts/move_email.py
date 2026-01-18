import argparse
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

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
            print("Error: Valid token not found.")
            return None

    return build('gmail', 'v1', credentials=creds)

def move_email(message_id, add_labels, remove_labels):
    service = get_service()
    if not service: return

    try:
        body = {
            'addLabelIds': add_labels,
            'removeLabelIds': remove_labels
        }
        # We need the ACTUAL Label IDs, not names, or we use the names if they are system labels
        # For custom labels, we need to find the ID first.
        
        # Get all labels to find IDs for names
        labels_result = service.users().labels().list(userId='me').execute()
        labels = labels_result.get('labels', [])
        
        final_add = []
        for label_name in add_labels:
            matched = [l['id'] for l in labels if l['name'].lower() == label_name.lower() or l['id'].lower() == label_name.lower()]
            if matched:
                final_add.append(matched[0])
            else:
                print(f"Warning: Label '{label_name}' not found.")

        final_remove = []
        for label_name in remove_labels:
            matched = [l['id'] for l in labels if l['name'].lower() == label_name.lower() or l['id'].lower() == label_name.lower()]
            if matched:
                final_remove.append(matched[0])

        body = {
            'addLabelIds': final_add,
            'removeLabelIds': final_remove
        }
        
        service.users().messages().modify(userId='me', id=message_id, body=body).execute()
        print(f"Successfully modified labels for message {message_id}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('message_id')
    parser.add_argument('--add', nargs='+')
    parser.add_argument('--remove', nargs='+')
    
    args = parser.parse_args()
    move_email(args.message_id, args.add or [], args.remove or [])
