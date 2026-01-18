#!/usr/bin/env python3
"""
Create multiple tasks from a JSON file.
"""

import sys
import json
import argparse
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from google_tasks_api import GoogleTasksAPI, format_task, print_json, parse_date

def parse_args():
    parser = argparse.ArgumentParser(description="Batch create tasks from JSON file")
    
    parser.add_argument(
        "--input-file",
        required=True,
        help="JSON file containing tasks to create"
    )
    
    parser.add_argument(
        "--list-id",
        help="Default task list ID if not specified in task (uses '@default' if not specified)"
    )
    
    return parser.parse_args()

def prepare_task(task_spec: dict) -> dict:
    """Prepare a task specification for API submission."""
    task_data = {
        "title": task_spec["title"]
    }
    
    # Notes
    if "notes" in task_spec:
        task_data["notes"] = task_spec["notes"]
    
    # Due date
    if "due_date" in task_spec:
        due_date = parse_date(task_spec["due_date"])
        if due_date:
            task_data["due"] = due_date
    
    # Parent (for subtasks)
    if "parent" in task_spec:
        task_data["parent"] = task_spec["parent"]
    
    return task_data

def main():
    args = parse_args()
    api = GoogleTasksAPI()
    
    # Use default list if not specified
    default_list_id = args.list_id or '@default'
    
    # Load tasks from file
    try:
        with open(args.input_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        return 1
    
    # Handle both array of tasks and object with tasks array
    if isinstance(data, list):
        tasks_to_create = data
    elif isinstance(data, dict) and "tasks" in data:
        tasks_to_create = data["tasks"]
    else:
        print("Error: Input file must contain an array of tasks or an object with 'tasks' key", file=sys.stderr)
        return 1
    
    # Create tasks
    results = []
    errors = []
    
    for i, task_spec in enumerate(tasks_to_create):
        try:
            # Get list ID for this task
            tasklist_id = task_spec.get("list_id", default_list_id)
            
            task_data = prepare_task(task_spec)
            result = api.create_task(tasklist_id, task_data)
            
            if result:
                results.append(format_task(result))
                print(f"✓ Created task {i+1}/{len(tasks_to_create)}: {task_spec['title']}", file=sys.stderr)
            else:
                errors.append({
                    "index": i,
                    "task": task_spec,
                    "error": "API returned None"
                })
                print(f"✗ Failed to create task {i+1}: {task_spec['title']}", file=sys.stderr)
        
        except Exception as e:
            errors.append({
                "index": i,
                "task": task_spec,
                "error": str(e)
            })
            print(f"✗ Error creating task {i+1}: {e}", file=sys.stderr)
    
    # Print summary
    print_json({
        "success": len(errors) == 0,
        "created": len(results),
        "failed": len(errors),
        "total": len(tasks_to_create),
        "tasks": results,
        "errors": errors
    })
    
    return 0 if len(errors) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
