#!/usr/bin/env python3
"""
Common utilities for Google Tasks API interactions.
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

SKILL_DIR = Path(__file__).parent.parent
TOKEN_FILE = SKILL_DIR / "token.json"
SCOPES = ['https://www.googleapis.com/auth/tasks']

class GoogleTasksAPI:
    """Wrapper for Google Tasks API operations."""
    
    def __init__(self):
        """Initialize the API client with stored credentials."""
        self.creds = self._load_credentials()
        self.service = build('tasks', 'v1', credentials=self.creds)
    
    def _load_credentials(self) -> Credentials:
        """Load and validate credentials from token file."""
        if not TOKEN_FILE.exists():
            print("Error: token.json not found. Please run auth.py first.", file=sys.stderr)
            sys.exit(1)
        
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        
        # Refresh if expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            TOKEN_FILE.write_text(creds.to_json())
        
        return creds
    
    def list_task_lists(self) -> Optional[List[Dict]]:
        """Get all task lists."""
        try:
            results = self.service.tasklists().list().execute()
            return results.get('items', [])
        except Exception as e:
            print(f"Error listing task lists: {e}", file=sys.stderr)
            return None
    
    def get_task_list(self, tasklist_id: str) -> Optional[Dict]:
        """Get a specific task list by ID."""
        try:
            return self.service.tasklists().get(tasklist=tasklist_id).execute()
        except Exception as e:
            print(f"Error getting task list: {e}", file=sys.stderr)
            return None
    
    def list_tasks(self, tasklist_id: str, show_completed: bool = False, 
                   show_hidden: bool = False, max_results: int = 100) -> Optional[List[Dict]]:
        """Get tasks from a task list."""
        try:
            results = self.service.tasks().list(
                tasklist=tasklist_id,
                showCompleted=show_completed,
                showHidden=show_hidden,
                maxResults=max_results
            ).execute()
            return results.get('items', [])
        except Exception as e:
            print(f"Error listing tasks: {e}", file=sys.stderr)
            return None
    
    def get_task(self, tasklist_id: str, task_id: str) -> Optional[Dict]:
        """Get a specific task by ID."""
        try:
            return self.service.tasks().get(
                tasklist=tasklist_id,
                task=task_id
            ).execute()
        except Exception as e:
            print(f"Error getting task: {e}", file=sys.stderr)
            return None
    
    def create_task(self, tasklist_id: str, task_data: Dict) -> Optional[Dict]:
        """Create a new task."""
        try:
            return self.service.tasks().insert(
                tasklist=tasklist_id,
                body=task_data
            ).execute()
        except Exception as e:
            print(f"Error creating task: {e}", file=sys.stderr)
            return None
    
    def update_task(self, tasklist_id: str, task_id: str, task_data: Dict) -> Optional[Dict]:
        """Update an existing task."""
        try:
            return self.service.tasks().update(
                tasklist=tasklist_id,
                task=task_id,
                body=task_data
            ).execute()
        except Exception as e:
            print(f"Error updating task: {e}", file=sys.stderr)
            return None
    
    def complete_task(self, tasklist_id: str, task_id: str) -> Optional[Dict]:
        """Mark a task as complete."""
        try:
            task = self.get_task(tasklist_id, task_id)
            if task:
                task['status'] = 'completed'
                return self.update_task(tasklist_id, task_id, task)
            return None
        except Exception as e:
            print(f"Error completing task: {e}", file=sys.stderr)
            return None
    
    def delete_task(self, tasklist_id: str, task_id: str) -> bool:
        """Delete a task."""
        try:
            self.service.tasks().delete(
                tasklist=tasklist_id,
                task=task_id
            ).execute()
            return True
        except Exception as e:
            print(f"Error deleting task: {e}", file=sys.stderr)
            return False

def format_task(task: Dict) -> Dict:
    """Format task data for display."""
    return {
        "id": task.get("id"),
        "title": task.get("title"),
        "notes": task.get("notes", ""),
        "status": task.get("status", "needsAction"),
        "due": task.get("due"),
        "completed": task.get("completed"),
        "parent": task.get("parent"),
        "position": task.get("position"),
        "updated": task.get("updated"),
        "self_link": task.get("selfLink")
    }

def format_task_list(tasklist: Dict) -> Dict:
    """Format task list data for display."""
    return {
        "id": tasklist.get("id"),
        "title": tasklist.get("title"),
        "updated": tasklist.get("updated"),
        "self_link": tasklist.get("selfLink")
    }

def parse_date(date_string: str) -> str:
    """Parse a date string into RFC 3339 format for Google Tasks API."""
    from dateutil import parser as date_parser
    try:
        dt = date_parser.parse(date_string)
        # Google Tasks expects RFC 3339 format (YYYY-MM-DDTHH:MM:SS.sssZ)
        return dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    except Exception as e:
        print(f"Warning: Could not parse date '{date_string}': {e}", file=sys.stderr)
        return None

def print_json(data: Any):
    """Print data as formatted JSON."""
    print(json.dumps(data, indent=2, ensure_ascii=False))
