#!/usr/bin/env python3
"""
List all databases accessible to the Notion integration.
"""

import json
import argparse
from utils import get_notion_client, format_rich_text

def main():
    parser = argparse.ArgumentParser(description="List all accessible Notion databases")
    args = parser.parse_args()
    
    try:
        notion = get_notion_client()
        
        # Search for databases
        results = notion.search(filter={"property": "object", "value": "database"})
        
        databases = []
        for db in results.get("results", []):
            db_info = {
                "id": db["id"],
                "title": format_rich_text(db.get("title", [])),
                "url": db.get("url"),
                "created_time": db.get("created_time"),
                "last_edited_time": db.get("last_edited_time"),
            }
            databases.append(db_info)
        
        output = {
            "success": True,
            "count": len(databases),
            "databases": databases
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
