#!/usr/bin/env python3
"""
List all Google Tasks task lists.
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from google_tasks_api import GoogleTasksAPI, format_task_list, print_json

def main():
    api = GoogleTasksAPI()
    
    task_lists = api.list_task_lists()
    
    if task_lists is None:
        print("Error: Failed to fetch task lists", file=sys.stderr)
        return 1
    
    # Format task lists for output
    formatted_lists = [format_task_list(tl) for tl in task_lists]
    
    # Sort by title
    formatted_lists.sort(key=lambda x: x["title"])
    
    print_json({
        "count": len(formatted_lists),
        "task_lists": formatted_lists
    })
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
