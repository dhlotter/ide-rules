#!/usr/bin/env python3
"""
Search across Notion workspace.
"""

import json
import argparse
from utils import get_notion_client, extract_page_properties, format_rich_text

def main():
    parser = argparse.ArgumentParser(description="Search Notion workspace")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--limit", type=int, default=20, help="Maximum number of results")
    parser.add_argument("--filter", choices=["page", "database"], help="Filter by object type")
    args = parser.parse_args()
    
    try:
        notion = get_notion_client()
        
        # Build search parameters
        search_params = {
            "query": args.query,
            "page_size": min(args.limit, 100)
        }
        
        if args.filter:
            search_params["filter"] = {
                "property": "object",
                "value": args.filter
            }
        
        # Perform search
        results = notion.search(**search_params)
        
        items = []
        for item in results.get("results", []):
            item_type = item.get("object")
            
            item_info = {
                "id": item["id"],
                "type": item_type,
                "url": item.get("url"),
                "created_time": item.get("created_time"),
                "last_edited_time": item.get("last_edited_time")
            }
            
            # Add title based on type
            if item_type == "page":
                item_info["properties"] = extract_page_properties(item)
                # Try to get a title from properties
                props = item_info["properties"]
                title = props.get("Name") or props.get("Title") or props.get("title") or "Untitled"
                item_info["title"] = title
            elif item_type == "database":
                item_info["title"] = format_rich_text(item.get("title", []))
            
            items.append(item_info)
        
        output = {
            "success": True,
            "query": args.query,
            "count": len(items),
            "has_more": results.get("has_more", False),
            "results": items
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
