#!/usr/bin/env python3
"""
Discover Supabase projects from the authenticated account
and update projects.json
"""

import sys
import re
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from supabase_api import SupabaseManager, print_result, print_error


def parse_projects_list(output):
    """
    Parses the output of 'supabase projects list'
    Example output lines:
    LINKED | ORG ID               | REFERENCE ID         | NAME               | REGION                   | CREATED AT (UTC)    
    -------|----------------------|----------------------|--------------------|--------------------------|---------------------
           | qjnjikomldfgfsqgtbpv | dcarxzpcogfflntthuwy | nymly-app          | East US (Ohio)           | 2025-10-11 22:13:47 
    """
    projects = []
    lines = output.strip().split('\n')
    
    # Simple regex to extract common project info
    # We look for lines with | separators that aren't headers/separators
    for line in lines:
        if '|' in line and not any(x in line for x in ['LINKED', 'ORG ID', '---']):
            # Split by | and strip whitespace
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4 and parts[2] and parts[3] and not parts[2].startswith('--'):
                # parts[0] is linked status
                # parts[1] is org id
                # parts[2] is reference id
                # parts[3] is name
                projects.append({
                    "ref": parts[2],
                    "name": parts[3]
                })
    return projects


def main():
    try:
        manager = SupabaseManager()
        
        # Run the CLI command to list projects
        res = manager.run_cli_command(["supabase", "projects", "list"])
        
        if not res["success"]:
            print_error(f"Failed to list projects: {res.get('error', 'Unknown error')}")
            
        projects_found = parse_projects_list(res["stdout"])
        
        for p in projects_found:
            manager.add_project(
                name=p["name"],
                ref=p["ref"]
            )
            
        result = {
            "discovered_count": len(projects_found),
            "projects": manager.list_projects(),
            "message": f"Successfully discovered {len(projects_found)} projects from your Supabase account."
        }
        
        print_result(result, "table")
        
    except Exception as e:
        print_error(str(e))


if __name__ == "__main__":
    main()
