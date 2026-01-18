#!/usr/bin/env python3
"""
Mark a task as complete in Google Tasks.
"""

import sys
import argparse
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from google_tasks_api import GoogleTasksAPI, format_task, print_json

def parse_args():
    parser = argparse.ArgumentParser(description="Mark a task as complete")
    
    parser.add_argument(
        "--task-id",
        required=True,
        help="Task ID to complete"
    )
    
    parser.add_argument(
        "--list-id",
        help="Task list ID (uses default list '@default' if not specified)"
    )
    
    return parser.parse_args()

def main():
    args = parse_args()
    api = GoogleTasksAPI()
    
    # Use default list if not specified
    tasklist_id = args.list_id or '@default'
    
    # Complete the task
    result = api.complete_task(tasklist_id, args.task_id)
    
    if result is None:
        print("Error: Failed to complete task", file=sys.stderr)
        return 1
    
    formatted_task = format_task(result)
    
    print_json({
        "success": True,
        "task": formatted_task,
        "message": "Task marked as complete"
    })
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
