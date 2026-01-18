#!/usr/bin/env python3
"""
Create a new database migration
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from supabase_api import SupabaseManager, print_result, print_error


def main():
    parser = argparse.ArgumentParser(description="Create new Supabase migration")
    parser.add_argument("--project", help="Project name (uses active project if not specified)")
    parser.add_argument("--name", required=True, help="Migration name")
    parser.add_argument("--format", choices=["json", "table"], default="json", help="Output format")
    
    args = parser.parse_args()
    
    try:
        manager = SupabaseManager(args.project)
        result = manager.create_migration(args.name, args.project)
        
        print_result(result, args.format)
        
    except Exception as e:
        print_error(str(e))


if __name__ == "__main__":
    main()
