import os.path
import base64
import json
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

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
            print("Error: Valid token not found. Please run auth.py first.")
            return None

    return build('gmail', 'v1', credentials=creds)

def clean_body(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text

def fetch_emails(limit=5, query="is:unread"):
    service = get_service()
    if not service:
        return

    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=limit).execute()
        messages = results.get('messages', [])

        email_data = []

        if not messages:
            print(json.dumps([]))
            return

        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            
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

            body = ""
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            data = part['body']['data']
                            body += base64.urlsafe_b64decode(data).decode('utf-8')
                    elif part['mimeType'] == 'text/html':
                         # Prefer plain text, but if only HTML exists or it's mixed, you might want logic here.
                         # For simple summarization, plain text is usually best.
                         pass
            elif 'body' in payload and 'data' in payload['body']:
                data = payload['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')

            # If body looks like HTML, clean it
            if "<html" in body.lower() or "<div" in body.lower():
                body = clean_body(body)

            email_data.append({
                'id': message['id'],
                'date': date,
                'from': sender,
                'subject': subject,
                'snippet': msg.get('snippet', ''),
                'body': body[:2000] # Truncate body to avoid hitting token limits downstream
            })

        print(json.dumps(email_data, indent=2))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch Gmail emails.')
    parser.add_argument('--limit', type=int, default=5, help='Number of emails to fetch')
    parser.add_argument('--query', type=str, default='is:unread', help='Gmail search query')
    
    args = parser.parse_args()
    fetch_emails(limit=args.limit, query=args.query)
