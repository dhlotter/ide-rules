#!/usr/bin/env python3
"""
Create a new entry in a Notion database.
"""

import json
import argparse
from utils import get_notion_client

def build_property(prop_name, prop_value, prop_type):
    """Build a property object based on type."""
    if prop_type == "title" or prop_type == "rich_text":
        return {
            prop_type: [
                {
                    "text": {
                        "content": prop_value
                    }
                }
            ]
        }
    elif prop_type == "number":
        return {"number": float(prop_value)}
    elif prop_type == "select":
        return {"select": {"name": prop_value}}
    elif prop_type == "multi_select":
        return {"multi_select": [{"name": name.strip()} for name in prop_value.split(",")]}
    elif prop_type == "checkbox":
        return {"checkbox": prop_value.lower() in ["true", "yes", "1"]}
    elif prop_type == "url":
        return {"url": prop_value}
    elif prop_type == "email":
        return {"email": prop_value}
    elif prop_type == "phone_number":
        return {"phone_number": prop_value}
    elif prop_type == "date":
        return {"date": {"start": prop_value}}
    else:
        # Default to rich_text
        return {
            "rich_text": [
                {
                    "text": {
                        "content": prop_value
                    }
                }
            ]
        }

def main():
    parser = argparse.ArgumentParser(description="Create a new database entry")
    parser.add_argument("--database-id", required=True, help="Database ID")
    parser.add_argument("--properties", required=True, help="Properties as JSON string")
    args = parser.parse_args()
    
    try:
        notion = get_notion_client()
        
        # Parse properties
        props_input = json.loads(args.properties)
        
        # Build properties object
        properties = {}
        for key, value in props_input.items():
            # Simple heuristic: if it's the first property or named "Name"/"Title", it's likely a title
            if key in ["Name", "Title", "name", "title"] and len(properties) == 0:
                properties[key] = {
                    "title": [
                        {
                            "text": {
                                "content": str(value)
                            }
                        }
                    ]
                }
            else:
                # Default to rich_text for simplicity
                properties[key] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": str(value)
                            }
                        }
                    ]
                }
        
        # Create the database entry
        new_page = notion.pages.create(
            parent={"database_id": args.database_id},
            properties=properties
        )
        
        output = {
            "success": True,
            "page_id": new_page["id"],
            "url": new_page.get("url"),
            "created_time": new_page.get("created_time")
        }
        
        print(json.dumps(output, indent=2))
        
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2))
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
