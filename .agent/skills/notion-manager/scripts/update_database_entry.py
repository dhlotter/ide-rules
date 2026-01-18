#!/usr/bin/env python3
"""
Update an existing database entry in Notion.
"""

import json
import argparse
from utils import get_notion_client

def main():
    parser = argparse.ArgumentParser(description="Update a database entry")
    parser.add_argument("--page-id", required=True, help="Page ID (database entry) to update")
    parser.add_argument("--properties", required=True, help="Properties to update as JSON string")
    args = parser.parse_args()
    
    try:
        notion = get_notion_client()
        
        # Parse properties
        props_input = json.loads(args.properties)
        
        # Build properties object
        properties = {}
        for key, value in props_input.items():
            # Simple approach: use rich_text for most properties
            # In practice, you'd want to inspect the database schema
            properties[key] = {
                "rich_text": [
                    {
                        "text": {
                            "content": str(value)
                        }
                    }
                ]
            }
        
        # Update the page
        updated_page = notion.pages.update(
            page_id=args.page_id,
            properties=properties
        )
        
        output = {
            "success": True,
            "page_id": updated_page["id"],
            "url": updated_page.get("url"),
            "last_edited_time": updated_page.get("last_edited_time")
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
