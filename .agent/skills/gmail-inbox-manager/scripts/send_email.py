import argparse
import os.path
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.compose']

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

def send_draft(draft_id):
    service = get_service()
    if not service: return

    try:
        sent_message = service.users().drafts().send(userId='me', body={'id': draft_id}).execute()
        print(f"Draft {draft_id} sent successfully. Message ID: {sent_message['id']}")
    except Exception as e:
        print(f"An error occurred while sending the draft: {e}")

def send_direct(to, subject, body, thread_id=None):
    service = get_service()
    if not service: return

    message = EmailMessage()
    message.set_content(body)
    message['To'] = to
    message['Subject'] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'raw': encoded_message}
    
    if thread_id:
        create_message['threadId'] = thread_id

    try:
        sent_message = service.users().messages().send(userId='me', body=create_message).execute()
        print(f"Message sent successfully. Message ID: {sent_message['id']}")
    except Exception as e:
        print(f"An error occurred while sending the message: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--draft_id')
    group.add_argument('--to')
    
    parser.add_argument('--subject')
    parser.add_argument('--body')
    parser.add_argument('--thread_id')
    
    args = parser.parse_args()
    
    if args.draft_id:
        send_draft(args.draft_id)
    else:
        if not args.subject or not args.body:
            print("Error: Subject and body are required for direct sending.")
        else:
            send_direct(args.to, args.subject, args.body, args.thread_id)
