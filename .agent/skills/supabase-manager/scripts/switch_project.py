#!/usr/bin/env python3
"""
Switch active Supabase project
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from supabase_api import SupabaseManager, print_result, print_error


def main():
    parser = argparse.ArgumentParser(description="Switch active Supabase project")
    parser.add_argument("--name", required=True, help="Project name to switch to")
    parser.add_argument("--format", choices=["json", "table"], default="json", help="Output format")
    
    args = parser.parse_args()
    
    try:
        manager = SupabaseManager()
        project = manager.switch_project(args.name)
        
        result = {
            "action": "switch",
            "active_project": project,
            "message": f"Switched to project '{args.name}'"
        }
        
        print_result(result, args.format)
        
    except Exception as e:
        print_error(str(e))


if __name__ == "__main__":
    main()
