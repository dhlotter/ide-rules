#!/usr/bin/env python3
"""
Create a dedicated task list for the Land Cruiser inspection.
"""

import sys
from google_tasks_api import GoogleTasksAPI, print_json

def create_inspection_task_list():
    """Create a new task list for the inspection with all items."""
    api = GoogleTasksAPI()
    
    # Create the new task list
    new_list = api.service.tasklists().insert(body={
        "title": "🔎 Land Cruiser Inspection"
    }).execute()
    
    if not new_list:
        print("Failed to create task list", file=sys.stderr)
        return False
    
    list_id = new_list['id']
    print(f"✅ Created task list: {new_list['title']}", file=sys.stderr)
    
    # Define all checklist items
    tasks = [
        # THE KILLERS
        "🛑 Chassis Rust - rear legs above axle",
        "🛑 Chassis Rust - inside rear wheel arches",
        "🛑 Chassis Rust - body mounts condition",
        "🛑 Windshield Frame - lift rubber seal",
        "🛑 Rain Gutters - check for bubbling",
        "🛑 Tailgate/Doors - bottom edges/hinges",
        "🛑 Panel Gaps - symmetric on bonnet/doors",
        "🛑 Front Chassis Legs - check for crinkles",
        "🛑 VIN Tag - matches papers, factory rivets",
        
        # THE KEEPERS
        "🟡 Diff Locks - rear/front engage properly",
        "🟡 Diff Leaks - check pinion seals",
        "🟡 Swivel Hubs - check for knuckle soup",
        "🟡 Panhardt Rods - check mounts for cracks",
        "🟡 Dashboard - check for cracks (R15k fix)",
        "🟡 Door Cards - intact, no water damage",
        "🟡 Windows - all 4 wind down smoothly",
        "🟡 Sunroof - opens/closes, no water stains",
        
        # RESALE VALUE
        "💰 Cold Start - smoke color check",
        "💰 Idle - smooth, no misfires",
        "💰 Oil Cap - check for mayonnaise",
        "💰 Paperwork - engine # matches papers",
        
        # QUESTIONS
        "🗣️ Invoice for 2019 engine rebuild?",
        "🗣️ Car lived in Melkbos whole life?",
        "🗣️ Diff locks factory or aftermarket?",
        "🗣️ Spare key available?"
    ]
    
    # Create each task
    for task_title in tasks:
        task = api.create_task(list_id, {"title": task_title})
        if task:
            print(f"  ✅ {task_title}", file=sys.stderr)
        else:
            print(f"  ❌ Failed: {task_title}", file=sys.stderr)
    
    print_json({
        "success": True,
        "list_id": list_id,
        "list_title": new_list['title'],
        "task_count": len(tasks),
        "message": "Inspection task list created successfully"
    })
    
    return True

if __name__ == "__main__":
    create_inspection_task_list()
