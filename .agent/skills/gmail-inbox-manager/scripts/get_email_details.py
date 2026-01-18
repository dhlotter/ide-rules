import os.path
import base64
import json
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

# Updated SCOPES to include modify for deletion, compose for draft, send for send
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

def clean_body(html_content):
    if html_content is None:
        return ""
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text

def get_email_details(message_id):
    service = get_service()
    if not service:
        return

    try:
        msg = service.users().messages().get(userId='me', id=message_id).execute()
        
        payload = msg['payload']
        headers = payload.get('headers', [])
        
        subject = ""
        sender = ""
        date = ""
        
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'From':
                sender = header['value']
            if header['name'] == 'Date':
                date = header['value']

        body_plain = ""
        body_html = ""
        attachments = []

        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body_plain = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                elif part['mimeType'] == 'text/html':
                    if 'data' in part['body']:
                        body_html = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                elif 'filename' in part and part['filename']:
                    attachments.append({
                        'filename': part['filename'],
                        'mimeType': part['mimeType'],
                        'attachmentId': part['body']['attachmentId']
                    })
        elif 'body' in payload and 'data' in payload['body']: # Case for emails without 'parts' but with a direct body
            if payload['mimeType'] == 'text/plain':
                body_plain = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
            elif payload['mimeType'] == 'text/html':
                body_html = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

        # Prioritize plain text, clean HTML if plain is empty
        body = body_plain if body_plain else clean_body(body_html)

        email_details = {
            'id': msg['id'],
            'date': date,
            'from': sender,
            'subject': subject,
            'body': body,
            'attachments': attachments
        }
        
        print(json.dumps(email_details, indent=2))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch full Gmail message details by ID.')
    parser.add_argument('message_id', help='The ID of the message to fetch.')
    
    args = parser.parse_args()
    get_email_details(args.message_id)
