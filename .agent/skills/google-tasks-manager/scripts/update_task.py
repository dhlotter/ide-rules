#!/usr/bin/env python3
"""
Update an existing task in Google Tasks.
"""

import sys
import argparse
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from google_tasks_api import GoogleTasksAPI, format_task, print_json, parse_date

def parse_args():
    parser = argparse.ArgumentParser(description="Update an existing task")
    
    parser.add_argument(
        "--task-id",
        required=True,
        help="Task ID to update"
    )
    
    parser.add_argument(
        "--list-id",
        help="Task list ID (uses default list '@default' if not specified)"
    )
    
    parser.add_argument(
        "--title",
        help="New task title"
    )
    
    parser.add_argument(
        "--notes",
        help="New task notes/description"
    )
    
    parser.add_argument(
        "--due-date",
        help="New due date in YYYY-MM-DD format"
    )
    
    parser.add_argument(
        "--status",
        choices=["needsAction", "completed"],
        help="New status"
    )
    
    return parser.parse_args()

def main():
    args = parse_args()
    api = GoogleTasksAPI()
    
    # Use default list if not specified
    tasklist_id = args.list_id or '@default'
    
    # Get current task
    current_task = api.get_task(tasklist_id, args.task_id)
    
    if current_task is None:
        print("Error: Failed to fetch current task", file=sys.stderr)
        return 1
    
    # Build update data (start with current task to preserve fields)
    update_data = current_task.copy()
    
    # Update only specified fields
    if args.title is not None:
        update_data["title"] = args.title
    
    if args.notes is not None:
        update_data["notes"] = args.notes
    
    if args.due_date is not None:
        due_date = parse_date(args.due_date)
        if due_date:
            update_data["due"] = due_date
    
    if args.status is not None:
        update_data["status"] = args.status
    
    # Update the task
    result = api.update_task(tasklist_id, args.task_id, update_data)
    
    if result is None:
        print("Error: Failed to update task", file=sys.stderr)
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
