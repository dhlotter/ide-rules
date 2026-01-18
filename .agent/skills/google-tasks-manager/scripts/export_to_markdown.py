#!/usr/bin/env python3
"""
Export Google Tasks to Markdown format for Obsidian.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from google_tasks_api import GoogleTasksAPI, format_task

def parse_args():
    parser = argparse.ArgumentParser(description="Export tasks to Markdown")
    
    parser.add_argument(
        "--list-id",
        help="Task list ID (uses default list '@default' if not specified)"
    )
    
    parser.add_argument(
        "--output-file",
        required=True,
        help="Output markdown file path"
    )
    
    parser.add_argument(
        "--status",
        choices=["needsAction", "completed", "all"],
        default="needsAction",
        help="Filter by status (default: needsAction)"
    )
    
    return parser.parse_args()

def format_task_markdown(task: dict, indent: int = 0) -> str:
    """Format a task as markdown."""
    lines = []
    prefix = "  " * indent
    
    # Checkbox and title
    checkbox = "- [x]" if task["status"] == "completed" else "- [ ]"
    title = task["title"]
    
    lines.append(f"{prefix}{checkbox} {title}")
    
    # Metadata
    metadata = []
    
    if task.get("due"):
        # Extract just the date part
        due_date = task["due"][:10] if len(task["due"]) >= 10 else task["due"]
        metadata.append(f"📅 {due_date}")
    
    if task.get("completed"):
        completed_date = task["completed"][:10] if len(task["completed"]) >= 10 else task["completed"]
        metadata.append(f"✅ {completed_date}")
    
    if metadata:
        lines.append(f"{prefix}  {' · '.join(metadata)}")
    
    # Notes/description
    if task.get("notes"):
        note_lines = task["notes"].split("\n")
        for line in note_lines:
            lines.append(f"{prefix}  {line}")
    
    return "\n".join(lines)

def main():
    args = parse_args()
    api = GoogleTasksAPI()
    
    # Use default list if not specified
    tasklist_id = args.list_id or '@default'
    
    # Get task list info
    task_list = api.get_task_list(tasklist_id)
    list_title = task_list.get("title", "Tasks") if task_list else "Tasks"
    
    # Determine if we should show completed tasks
    show_completed = args.status in ["completed", "all"]
    
    # Fetch tasks
    tasks = api.list_tasks(
        tasklist_id=tasklist_id,
        show_completed=show_completed,
        max_results=100
    )
    
    if tasks is None:
        print("Error: Failed to fetch tasks", file=sys.stderr)
        return 1
    
    # Format tasks
    formatted_tasks = [format_task(t) for t in tasks]
    
    # Filter by status if needed
    if args.status == "needsAction":
        formatted_tasks = [t for t in formatted_tasks if t["status"] != "completed"]
    elif args.status == "completed":
        formatted_tasks = [t for t in formatted_tasks if t["status"] == "completed"]
    
    # Sort by due date (tasks with no due date go last)
    formatted_tasks.sort(
        key=lambda x: x.get("due") or "9999-12-31T23:59:59.000Z"
    )
    
    # Build markdown content
    lines = []
    
    # Header
    lines.append(f"# {list_title}")
    lines.append("")
    lines.append(f"*Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    lines.append("")
    lines.append(f"**Total Tasks:** {len(formatted_tasks)}")
    lines.append(f"**Status Filter:** {args.status}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Group by due date
    today = datetime.now().strftime('%Y-%m-%d')
    
    overdue = []
    due_today = []
    upcoming = []
    no_due_date = []
    
    for task in formatted_tasks:
        if task.get("due"):
            due_date = task["due"][:10]
            if due_date < today:
                overdue.append(task)
            elif due_date == today:
                due_today.append(task)
            else:
                upcoming.append(task)
        else:
            no_due_date.append(task)
    
    # Overdue tasks
    if overdue:
        lines.append("## ⚠️ Overdue")
        lines.append("")
        for task in overdue:
            lines.append(format_task_markdown(task))
            lines.append("")
    
    # Due today
    if due_today:
        lines.append("## 📅 Due Today")
        lines.append("")
        for task in due_today:
            lines.append(format_task_markdown(task))
            lines.append("")
    
    # Upcoming
    if upcoming:
        lines.append("## 📆 Upcoming")
        lines.append("")
        for task in upcoming:
            lines.append(format_task_markdown(task))
            lines.append("")
    
    # No due date
    if no_due_date:
        lines.append("## 📋 No Due Date")
        lines.append("")
        for task in no_due_date:
            lines.append(format_task_markdown(task))
            lines.append("")
    
    # Write to file
    markdown_content = "\n".join(lines)
    
    try:
        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown_content)
        
        print(f"✓ Exported {len(formatted_tasks)} tasks to {args.output_file}", file=sys.stderr)
        
        # Also print JSON summary
        import json
        print(json.dumps({
            "success": True,
            "output_file": str(output_path),
            "task_count": len(formatted_tasks),
            "list_title": list_title
        }, indent=2))
        
        return 0
    
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
