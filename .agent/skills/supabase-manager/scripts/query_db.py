#!/usr/bin/env python3
"""
Execute SQL queries against Supabase database
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from supabase_api import SupabaseManager, print_result, print_error


def main():
    parser = argparse.ArgumentParser(description="Execute SQL query on Supabase database")
    parser.add_argument("--project", help="Project name (uses active project if not specified)")
    parser.add_argument("--query", help="SQL query to execute")
    parser.add_argument("--file", help="Path to SQL file to execute")
    parser.add_argument("--format", choices=["json", "table"], default="json", help="Output format")
    
    args = parser.parse_args()
    
    if not args.query and not args.file:
        print_error("Either --query or --file must be specified")
    
    try:
        manager = SupabaseManager(args.project)
        
        # Get query from file or argument
        if args.file:
            with open(args.file, 'r') as f:
                query = f.read()
        else:
            query = args.query
        
        result = manager.execute_sql(query, args.project)
        
        print_result(result, args.format)
        
    except Exception as e:
        print_error(str(e))


if __name__ == "__main__":
    main()
