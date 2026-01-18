#!/usr/bin/env python3
"""
Query entries from a Notion database.
"""

import json
import argparse
from utils import get_notion_client, extract_page_properties

def main():
    parser = argparse.ArgumentParser(description="Query entries from a Notion database")
    parser.add_argument("--database-id", required=True, help="Database ID to query")
    parser.add_argument("--limit", type=int, default=100, help="Maximum number of entries to return")
    parser.add_argument("--filter", help="Filter as JSON string (optional)")
    parser.add_argument("--sorts", help="Sort criteria as JSON string (optional)")
    args = parser.parse_args()
    
    try:
        notion = get_notion_client()
        
        # Build query parameters
        query_params = {
            "database_id": args.database_id,
            "page_size": min(args.limit, 100)
        }
        
        if args.filter:
            query_params["filter"] = json.loads(args.filter)
        
        if args.sorts:
            query_params["sorts"] = json.loads(args.sorts)
        
        # Query the database
        results = notion.databases.query(**query_params)
        
        entries = []
        for page in results.get("results", []):
            entry = {
                "id": page["id"],
                "url": page.get("url"),
                "created_time": page.get("created_time"),
                "last_edited_time": page.get("last_edited_time"),
                "properties": extract_page_properties(page)
            }
            entries.append(entry)
        
        output = {
            "success": True,
            "database_id": args.database_id,
            "count": len(entries),
            "has_more": results.get("has_more", False),
            "entries": entries
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
