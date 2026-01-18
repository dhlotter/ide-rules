#!/usr/bin/env python3
"""
Shared utilities for Notion Manager scripts.
"""

import os
import sys
import json
from pathlib import Path
from notion_client import Client

def get_token():
    """Read the Notion integration token from token.txt."""
    script_dir = Path(__file__).parent.parent
    token_file = script_dir / "token.txt"
    
    if not token_file.exists():
        print(json.dumps({
            "error": "Token file not found. Run setup.py first.",
            "success": False
        }), file=sys.stderr)
        sys.exit(1)
    
    token = token_file.read_text().strip()
    if not token:
        print(json.dumps({
            "error": "Token file is empty. Run setup.py first.",
            "success": False
        }), file=sys.stderr)
        sys.exit(1)
    
    return token

def get_notion_client():
    """Create and return a Notion client."""
    token = get_token()
    return Client(auth=token)

def format_rich_text(rich_text_array):
    """Extract plain text from Notion rich text array."""
    if not rich_text_array:
        return ""
    return "".join([text.get("plain_text", "") for text in rich_text_array])

def format_property_value(prop):
    """Extract value from a Notion property object."""
    prop_type = prop.get("type")
    
    if prop_type == "title":
        return format_rich_text(prop.get("title", []))
    elif prop_type == "rich_text":
        return format_rich_text(prop.get("rich_text", []))
    elif prop_type == "number":
        return prop.get("number")
    elif prop_type == "select":
        select = prop.get("select")
        return select.get("name") if select else None
    elif prop_type == "multi_select":
        return [item.get("name") for item in prop.get("multi_select", [])]
    elif prop_type == "date":
        date = prop.get("date")
        if date:
            return {
                "start": date.get("start"),
                "end": date.get("end")
            }
        return None
    elif prop_type == "checkbox":
        return prop.get("checkbox")
    elif prop_type == "url":
        return prop.get("url")
    elif prop_type == "email":
        return prop.get("email")
    elif prop_type == "phone_number":
        return prop.get("phone_number")
    elif prop_type == "status":
        status = prop.get("status")
        return status.get("name") if status else None
    elif prop_type == "people":
        return [person.get("name", person.get("id")) for person in prop.get("people", [])]
    elif prop_type == "files":
        return [file.get("name") for file in prop.get("files", [])]
    elif prop_type == "relation":
        return [rel.get("id") for rel in prop.get("relation", [])]
    else:
        return None

def extract_page_properties(page):
    """Extract properties from a page object into a clean dictionary."""
    properties = {}
    for key, value in page.get("properties", {}).items():
        properties[key] = format_property_value(value)
    return properties

def format_block_content(block):
    """Format a block's content into readable text."""
    block_type = block.get("type")
    content = block.get(block_type, {})
    
    # Most blocks have rich_text
    if "rich_text" in content:
        return format_rich_text(content["rich_text"])
    
    # Special cases
    if block_type == "child_page":
        return f"[Child Page: {content.get('title', 'Untitled')}]"
    elif block_type == "child_database":
        return f"[Child Database: {content.get('title', 'Untitled')}]"
    elif block_type == "image":
        return f"[Image: {content.get('caption', 'No caption')}]"
    elif block_type == "file":
        return f"[File: {content.get('caption', 'No caption')}]"
    elif block_type == "bookmark":
        return f"[Bookmark: {content.get('url', '')}]"
    elif block_type == "divider":
        return "---"
    
    return ""
