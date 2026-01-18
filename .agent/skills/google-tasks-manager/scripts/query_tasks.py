#!/usr/bin/env python3
"""
Query tasks from Google Tasks with optional filters.
"""

import sys
import argparse
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from google_tasks_api import GoogleTasksAPI, format_task, print_json

def parse_args():
    parser = argparse.ArgumentParser(description="Query tasks from Google Tasks")
    
    parser.add_argument(
        "--list-id",
        help="Task list ID (uses default list '@default' if not specified)"
    )
    
    parser.add_argument(
        "--status",
        choices=["needsAction", "completed", "all"],
        default="needsAction",
        help="Filter by status (default: needsAction)"
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of tasks to return (default: 50)"
    )
    
    return parser.parse_args()

def main():
    args = parse_args()
    api = GoogleTasksAPI()
    
    # Use default list if not specified
    tasklist_id = args.list_id or '@default'
    
    # Determine if we should show completed tasks
    show_completed = args.status in ["completed", "all"]
    
    # Fetch tasks
    tasks = api.list_tasks(
        tasklist_id=tasklist_id,
        show_completed=show_completed,
        max_results=args.limit
    )
    
    if tasks is None:
        print("Error: Failed to fetch tasks", file=sys.stderr)
        return 1
    
    # Filter by status if needed
    if args.status == "needsAction":
        tasks = [t for t in tasks if t.get("status") != "completed"]
    elif args.status == "completed":
        tasks = [t for t in tasks if t.get("status") == "completed"]
    
    # Format tasks
    formatted_tasks = [format_task(t) for t in tasks]
    
    # Sort by due date (tasks with no due date go last)
    formatted_tasks.sort(
        key=lambda x: x.get("due") or "9999-12-31T23:59:59.000Z"
    )
    
    print_json({
        "count": len(formatted_tasks),
        "list_id": tasklist_id,
        "filters": {
            "status": args.status,
            "limit": args.limit
        },
        "tasks": formatted_tasks
    })
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
