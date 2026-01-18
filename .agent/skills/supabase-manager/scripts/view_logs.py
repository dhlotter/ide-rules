#!/usr/bin/env python3
"""
View Supabase logs
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from supabase_api import SupabaseManager, print_result, print_error


def main():
    parser = argparse.ArgumentParser(description="View Supabase logs")
    parser.add_argument("--project", help="Project name (uses active project if not specified)")
    parser.add_argument("--type", 
                       choices=["all", "api", "db", "auth", "realtime", "storage", "functions"],
                       default="all",
                       help="Log type to view")
    parser.add_argument("--hours", type=int, default=1, help="Hours of logs to retrieve (default: 1)")
    parser.add_argument("--level", choices=["debug", "info", "warn", "error"], help="Filter by log level")
    parser.add_argument("--tail", action="store_true", help="Follow logs in real-time")
    parser.add_argument("--format", choices=["json", "table"], default="json", help="Output format")
    
    args = parser.parse_args()
    
    try:
        manager = SupabaseManager(args.project)
        
        if args.tail:
            # For tail mode, we'll use the CLI directly
            cmd = ["supabase", "logs"]
            if args.type != "all":
                cmd.extend(["--type", args.type])
            if args.level:
                cmd.extend(["--level", args.level])
            cmd.append("--tail")
            
            result = manager.run_cli_command(cmd)
            print(result.get("stdout", ""))
        else:
            result = manager.get_logs(args.type, args.hours, args.project)
            
            if args.level and result.get("success"):
                # Filter logs by level if specified
                result["filtered_by_level"] = args.level
            
            print_result(result, args.format)
        
    except Exception as e:
        print_error(str(e))


if __name__ == "__main__":
    main()
