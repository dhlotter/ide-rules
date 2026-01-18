#!/usr/bin/env python3
"""
Create a new task in Google Tasks.
"""

import sys
import argparse
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from google_tasks_api import GoogleTasksAPI, format_task, print_json, parse_date

def parse_args():
    parser = argparse.ArgumentParser(description="Create a new task in Google Tasks")
    
    parser.add_argument(
        "--title",
        required=True,
        help="Task title (required)"
    )
    
    parser.add_argument(
        "--notes",
        default="",
        help="Task notes/description"
    )
    
    parser.add_argument(
        "--list-id",
        help="Task list ID (uses default list '@default' if not specified)"
    )
    
    parser.add_argument(
        "--due-date",
        help="Due date in YYYY-MM-DD format or natural language"
    )
    
    parser.add_argument(
        "--parent",
        help="Parent task ID (for subtasks)"
    )
    
    return parser.parse_args()

def main():
    args = parse_args()
    api = GoogleTasksAPI()
    
    # Use default list if not specified
    tasklist_id = args.list_id or '@default'
    
    # Build task data
    task_data = {
        "title": args.title
    }
    
    # Add optional fields
    if args.notes:
        task_data["notes"] = args.notes
    
    if args.due_date:
        due_date = parse_date(args.due_date)
        if due_date:
            task_data["due"] = due_date
    
    if args.parent:
        task_data["parent"] = args.parent
    
    # Create the task
    result = api.create_task(tasklist_id, task_data)
    
    if result is None:
        print("Error: Failed to create task", file=sys.stderr)
        return 1
    
    # Format and print result
    formatted_task = format_task(result)
    
    print_json({
        "success": True,
        "task": formatted_task
    })
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
