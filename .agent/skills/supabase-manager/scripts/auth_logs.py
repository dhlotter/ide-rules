#!/usr/bin/env python3
"""
View authentication logs
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from supabase_api import SupabaseManager, print_result, print_error


def main():
    parser = argparse.ArgumentParser(description="View Supabase authentication logs")
    parser.add_argument("--project", help="Project name (uses active project if not specified)")
    parser.add_argument("--hours", type=int, default=24, help="Hours of logs to retrieve (default: 24)")
    parser.add_argument("--filter", choices=["all", "failed", "success"], default="all", help="Filter by auth result")
    parser.add_argument("--format", choices=["json", "table"], default="json", help="Output format")
    
    args = parser.parse_args()
    
    try:
        manager = SupabaseManager(args.project)
        result = manager.get_logs("auth", args.hours, args.project)
        
        if result.get("success"):
            result["filter"] = args.filter
        
        print_result(result, args.format)
        
    except Exception as e:
        print_error(str(e))


if __name__ == "__main__":
    main()
