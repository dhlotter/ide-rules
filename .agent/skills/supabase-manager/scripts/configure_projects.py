#!/usr/bin/env python3
"""
Configure Supabase projects
Add, remove, or update project configurations
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from supabase_api import SupabaseManager, print_result, print_error


def main():
    parser = argparse.ArgumentParser(description="Configure Supabase projects")
    parser.add_argument("--add", action="store_true", help="Add a new project")
    parser.add_argument("--remove", action="store_true", help="Remove a project")
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument("--ref", help="Project reference ID")
    parser.add_argument("--path", help="Project path on local machine")
    parser.add_argument("--url", help="Project URL (optional, will be generated from ref)")
    parser.add_argument("--format", choices=["json", "table"], default="json", help="Output format")
    
    args = parser.parse_args()
    
    try:
        manager = SupabaseManager()
        
        if args.add:
            if not args.ref:
                print_error("--ref is required when adding a project")
            
            project = manager.add_project(
                name=args.name,
                ref=args.ref,
                path=args.path,
                url=args.url
            )
            
            result = {
                "action": "add",
                "project": project,
                "message": f"Project '{args.name}' added successfully"
            }
            
        elif args.remove:
            # Remove project from configuration
            projects = manager.list_projects()
            manager.projects["projects"] = [p for p in projects if p["name"] != args.name]
            
            # Update active project if we removed it
            if manager.projects.get("active_project") == args.name:
                if manager.projects["projects"]:
                    manager.projects["active_project"] = manager.projects["projects"][0]["name"]
                else:
                    manager.projects["active_project"] = None
            
            manager._save_projects()
            
            result = {
                "action": "remove",
                "project_name": args.name,
                "message": f"Project '{args.name}' removed successfully"
            }
        else:
            print_error("Please specify --add or --remove")
        
        print_result(result, args.format)
        
    except Exception as e:
        print_error(str(e))


if __name__ == "__main__":
    main()
