import argparse
import os.path
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

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

def create_draft(to, subject, body, thread_id=None):
    service = get_service()
    if not service: return

    message = EmailMessage()
    message.set_content(body)
    message['To'] = to
    message['Subject'] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {
        'message': {
            'raw': encoded_message
        }
    }
    
    if thread_id:
        create_message['message']['threadId'] = thread_id

    try:
        draft = service.users().drafts().create(userId='me', body=create_message).execute()
        print(f"Draft created successfully. Draft ID: {draft['id']}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--to', required=True)
    parser.add_argument('--subject', required=True)
    parser.add_argument('--body', required=True)
    parser.add_argument('--thread_id')
    
    args = parser.parse_args()
    create_draft(args.to, args.subject, args.body, args.thread_id)
