#!/usr/bin/env python3
"""
Create a new page in Notion.
"""

import json
import argparse
from utils import get_notion_client

def main():
    parser = argparse.ArgumentParser(description="Create a new Notion page")
    parser.add_argument("--parent-id", required=True, help="Parent page or database ID")
    parser.add_argument("--title", required=True, help="Page title")
    parser.add_argument("--content", help="Page content (plain text)")
    parser.add_argument("--parent-type", choices=["page", "database"], default="page", 
                       help="Type of parent (page or database)")
    args = parser.parse_args()
    
    try:
        notion = get_notion_client()
        
        # Build parent reference
        if args.parent_type == "database":
            parent = {"database_id": args.parent_id}
        else:
            parent = {"page_id": args.parent_id}
        
        # Build properties
        properties = {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": args.title
                        }
                    }
                ]
            }
        }
        
        # Build children (content blocks)
        children = []
        if args.content:
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": args.content
                            }
                        }
                    ]
                }
            })
        
        # Create the page
        new_page = notion.pages.create(
            parent=parent,
            properties=properties,
            children=children if children else None
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
