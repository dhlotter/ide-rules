import argparse
import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dateutil import parser as date_parser

SCOPES = ['https://www.googleapis.com/auth/calendar']

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

    return build('calendar', 'v3', credentials=creds)

def add_event(summary, start_time, end_time=None, description=None, location=None):
    service = get_service()
    if not service: return

    # Parse dates
    start = date_parser.parse(start_time)
    if end_time:
        end = date_parser.parse(end_time)
    else:
        end = start + datetime.timedelta(hours=1)

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': 'UTC', # Defaulting to UTC for now, or user can specify in string
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': 'UTC',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")
    print(f"Event ID: {event.get('id')}")

def list_events(limit=10):
    service = get_service()
    if not service: return

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print(f'Getting the upcoming {limit} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=limit, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"{start} - {event['summary']} ({event['id']})")

def delete_event(event_id):
    service = get_service()
    if not service: return

    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(f"Event {event_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting event: {e}")

def update_event(event_id, summary=None, start_time=None, end_time=None, description=None):
    service = get_service()
    if not service: return

    # First fetch the event
    event = service.events().get(calendarId='primary', eventId=event_id).execute()

    if summary: event['summary'] = summary
    if description: event['description'] = description
    
    if start_time:
        start = date_parser.parse(start_time)
        event['start']['dateTime'] = start.isoformat()
    if end_time:
        end = date_parser.parse(end_time)
        event['end']['dateTime'] = end.isoformat()

    updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    print(f"Event updated: {updated_event.get('htmlLink')}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage Google Calendar events.')
    subparsers = parser.add_subparsers(dest='command')

    # Add event
    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('--summary', required=True)
    add_parser.add_argument('--start', required=True)
    add_parser.add_argument('--end')
    add_parser.add_argument('--description')
    add_parser.add_argument('--location')

    # List events
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('--limit', type=int, default=10)

    # Delete event
    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('--id', required=True)

    # Update event
    update_parser = subparsers.add_parser('update')
    update_parser.add_argument('--id', required=True)
    update_parser.add_argument('--summary')
    update_parser.add_argument('--start')
    update_parser.add_argument('--end')
    update_parser.add_argument('--description')

    args = parser.parse_args()

    if args.command == 'add':
        add_event(args.summary, args.start, args.end, args.description, args.location)
    elif args.command == 'list':
        list_events(args.limit)
    elif args.command == 'delete':
        delete_event(args.id)
    elif args.command == 'update':
        update_event(args.id, args.summary, args.start, args.end, args.description)
