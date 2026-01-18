#!/usr/bin/env python3
"""
Read the content of a Notion page.
"""

import json
import argparse
from utils import get_notion_client, extract_page_properties, format_block_content

def main():
    parser = argparse.ArgumentParser(description="Read a Notion page")
    parser.add_argument("--page-id", required=True, help="Page ID to read")
    parser.add_argument("--include-children", action="store_true", help="Include child blocks")
    args = parser.parse_args()
    
    try:
        notion = get_notion_client()
        
        # Get the page
        page = notion.pages.retrieve(page_id=args.page_id)
        
        # Extract basic info
        page_info = {
            "id": page["id"],
            "url": page.get("url"),
            "created_time": page.get("created_time"),
            "last_edited_time": page.get("last_edited_time"),
            "properties": extract_page_properties(page)
        }
        
        # Get page content (blocks)
        if args.include_children:
            blocks = []
            block_results = notion.blocks.children.list(block_id=args.page_id)
            
            for block in block_results.get("results", []):
                block_info = {
                    "id": block["id"],
                    "type": block["type"],
                    "content": format_block_content(block),
                    "has_children": block.get("has_children", False)
                }
                blocks.append(block_info)
            
            page_info["blocks"] = blocks
            page_info["block_count"] = len(blocks)
        
        output = {
            "success": True,
            "page": page_info
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
