#!/usr/bin/env python3
"""
List all configured Supabase projects
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from supabase_api import SupabaseManager, print_result, print_error


def main():
    parser = argparse.ArgumentParser(description="List all Supabase projects")
    parser.add_argument("--format", choices=["json", "table"], default="json", help="Output format")
    
    args = parser.parse_args()
    
    try:
        manager = SupabaseManager()
        projects = manager.list_projects()
        
        result = {
            "projects": projects,
            "active_project": manager.projects.get("active_project"),
            "count": len(projects)
        }
        
        print_result(result, args.format)
        
    except Exception as e:
        print_error(str(e))


if __name__ == "__main__":
    main()
