#!/usr/bin/env python3
"""
Update an existing Notion page.
"""

import json
import argparse
from utils import get_notion_client

def main():
    parser = argparse.ArgumentParser(description="Update a Notion page")
    parser.add_argument("--page-id", required=True, help="Page ID to update")
    parser.add_argument("--title", help="New title")
    parser.add_argument("--append-content", help="Content to append as a new paragraph")
    parser.add_argument("--archived", action="store_true", help="Archive the page")
    args = parser.parse_args()
    
    try:
        notion = get_notion_client()
        
        # Update properties if title provided
        if args.title:
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
            
            notion.pages.update(
                page_id=args.page_id,
                properties=properties
            )
        
        # Archive if requested
        if args.archived:
            notion.pages.update(
                page_id=args.page_id,
                archived=True
            )
        
        # Append content if provided
        if args.append_content:
            notion.blocks.children.append(
                block_id=args.page_id,
                children=[
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": args.append_content
                                    }
                                }
                            ]
                        }
                    }
                ]
            )
        
        # Get updated page
        updated_page = notion.pages.retrieve(page_id=args.page_id)
        
        output = {
            "success": True,
            "page_id": updated_page["id"],
            "url": updated_page.get("url"),
            "last_edited_time": updated_page.get("last_edited_time"),
            "archived": updated_page.get("archived", False)
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
