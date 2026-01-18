#!/usr/bin/env python3
"""
Inspect database schema
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from supabase_api import SupabaseManager, print_result, print_error


def main():
    parser = argparse.ArgumentParser(description="Inspect Supabase database schema")
    parser.add_argument("--project", help="Project name (uses active project if not specified)")
    parser.add_argument("--table", help="Specific table to inspect (optional)")
    parser.add_argument("--schema", default="public", help="Schema name (default: public)")
    parser.add_argument("--format", choices=["json", "table"], default="json", help="Output format")
    
    args = parser.parse_args()
    
    try:
        manager = SupabaseManager(args.project)
        
        if args.table:
            # Get detailed table information
            query = f"""
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = '{args.schema}'
              AND table_name = '{args.table}'
            ORDER BY ordinal_position;
            """
        else:
            # List all tables
            query = f"""
            SELECT 
                table_name,
                table_type
            FROM information_schema.tables
            WHERE table_schema = '{args.schema}'
            ORDER BY table_name;
            """
        
        result = manager.execute_sql(query, args.project)
        
        if result["success"]:
            result["schema"] = args.schema
            result["table"] = args.table
        
        print_result(result, args.format)
        
    except Exception as e:
        print_error(str(e))


if __name__ == "__main__":
    main()
