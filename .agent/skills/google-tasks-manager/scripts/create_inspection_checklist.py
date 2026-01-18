#!/usr/bin/env python3
"""
Create a structured inspection checklist task with subtasks.
"""

import sys
from google_tasks_api import GoogleTasksAPI, print_json

def create_inspection_checklist(list_id: str):
    """Create the Land Cruiser inspection checklist with subtasks."""
    api = GoogleTasksAPI()
    
    # Create main task
    main_task = api.create_task(list_id, {
        "title": "🔎 Land Cruiser Inspection - Chris (Melkbos)",
        "notes": "Donor vehicle inspection for M57 swap project.\n\nReference: 20-Projects/2026-01-16-land-cruiser-80/Inspection-Checklist-Chris.md"
    })
    
    if not main_task:
        print("Failed to create main task", file=sys.stderr)
        return False
    
    main_task_id = main_task['id']
    print(f"✅ Created main task: {main_task['title']}", file=sys.stderr)
    
    # Define subtask structure
    sections = [
        {
            "title": "🛑 THE KILLERS (Walk Away Items)",
            "subtasks": [
                "Chassis Rust - rear legs above axle",
                "Chassis Rust - inside rear wheel arches",
                "Chassis Rust - body mounts condition",
                "Windshield Frame - lift rubber seal",
                "Rain Gutters - check for bubbling",
                "Tailgate/Doors - bottom edges/hinges",
                "Panel Gaps - symmetric on bonnet/doors",
                "Front Chassis Legs - check for crinkles",
                "VIN Tag - matches papers, factory rivets"
            ]
        },
        {
            "title": "🟡 THE KEEPERS (Must be Solid)",
            "subtasks": [
                "Diff Locks - rear/front engage properly",
                "Diff Leaks - check pinion seals",
                "Swivel Hubs - check for knuckle soup",
                "Panhardt Rods - check mounts for cracks",
                "Dashboard - check for cracks (R15k fix)",
                "Door Cards - intact, no water damage",
                "Windows - all 4 wind down smoothly",
                "Sunroof - opens/closes, no water stains"
            ]
        },
        {
            "title": "💰 RESALE VALUE (The Engine)",
            "subtasks": [
                "Cold Start - smoke color check",
                "Idle - smooth, no misfires",
                "Oil Cap - check for mayonnaise",
                "Paperwork - engine # matches papers"
            ]
        },
        {
            "title": "🗣️ QUESTIONS FOR SELLER",
            "subtasks": [
                "Invoice for 2019 engine rebuild?",
                "Car lived in Melkbos whole life?",
                "Diff locks factory or aftermarket?",
                "Spare key available?"
            ]
        }
    ]
    
    # Create section headers and their subtasks
    for section in sections:
        # Create section header as subtask of main task
        section_task = api.create_task(list_id, {
            "title": section["title"],
            "parent": main_task_id
        })
        
        if not section_task:
            print(f"Failed to create section: {section['title']}", file=sys.stderr)
            continue
        
        section_task_id = section_task['id']
        print(f"  ✅ Created section: {section['title']}", file=sys.stderr)
        
        # Create individual checklist items as subtasks of the section
        for item in section["subtasks"]:
            item_task = api.create_task(list_id, {
                "title": item,
                "parent": section_task_id
            })
            
            if item_task:
                print(f"    ✅ Created item: {item}", file=sys.stderr)
            else:
                print(f"    ❌ Failed to create item: {item}", file=sys.stderr)
    
    # Return the main task details
    print_json({
        "success": True,
        "main_task_id": main_task_id,
        "message": "Inspection checklist created successfully"
    })
    
    return True

if __name__ == "__main__":
    # Use the Inbox list ID
    INBOX_LIST_ID = "MTc5MTUzNTc0NjM5NjkxNDAyNjM6MDow"
    
    create_inspection_checklist(INBOX_LIST_ID)
