import os.path
import base64
import json
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

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

def download_attachment(message_id, attachment_id, filename, save_path):
    service = get_service()
    if not service:
        return

    try:
        attachment = service.users().messages().attachments().get(
            userId='me', messageId=message_id, id=attachment_id).execute()
        
        file_data = base64.urlsafe_b64decode(attachment['data'])

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(file_data)
        
        print(f"Attachment '{filename}' saved to '{save_path}'")
        return save_path

    except Exception as e:
        print(f"An error occurred downloading attachment: {e}")
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download Gmail message attachment.')
    parser.add_argument('--message_id', required=True, help='The ID of the message containing the attachment.')
    parser.add_argument('--attachment_id', required=True, help='The ID of the attachment to download.')
    parser.add_argument('--filename', required=True, help='The original filename of the attachment.')
    parser.add_argument('--save_dir', required=True, help='The directory to save the attachment.')
    
    args = parser.parse_args()
    save_path = os.path.join(args.save_dir, args.filename)
    download_attachment(args.message_id, args.attachment_id, args.filename, save_path)
