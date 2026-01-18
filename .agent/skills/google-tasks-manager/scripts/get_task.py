#!/usr/bin/env python3
"""
Get detailed information about a specific task.
"""

import sys
import argparse
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from google_tasks_api import GoogleTasksAPI, format_task, print_json

def parse_args():
    parser = argparse.ArgumentParser(description="Get task details")
    
    parser.add_argument(
        "--task-id",
        required=True,
        help="Task ID to retrieve"
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
    
    # Get the task
    task = api.get_task(tasklist_id, args.task_id)
    
    if task is None:
        print("Error: Failed to fetch task", file=sys.stderr)
        return 1
    
    # Format and print result
    formatted_task = format_task(task)
    
    print_json({
        "success": True,
        "task": formatted_task
    })
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
