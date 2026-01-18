#!/usr/bin/env python3
"""
Detect which Supabase project the current directory is linked to
by reading .supabase/project-ref
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from supabase_api import SupabaseManager, print_result, print_error


def find_project_ref(start_path):
    """Search for .supabase/project-ref in current and parent directories"""
    current = Path(start_path).resolve()
    while current != current.parent:
        ref_file = current / ".supabase" / "project-ref"
        if ref_file.exists():
            with open(ref_file, 'r') as f:
                return f.read().strip(), current
        current = current.parent
    return None, None


def main():
    try:
        manager = SupabaseManager()
        
        # Look for project-ref in current or parent dirs
        ref, path = find_project_ref(os.getcwd())
        
        if not ref:
            print_result({
                "success": False,
                "message": "No .supabase/project-ref found in this directory or its parents. Is the project linked?"
            })
            return

        # Find project name by ref in our config
        all_projects = manager.list_projects()
        target_project = None
        for p in all_projects:
            if p["ref"] == ref:
                target_project = p
                break
        
        if target_project:
            # Switch to it
            manager.switch_project(target_project["name"])
            # Update path in case it changed
            for p in manager.projects["projects"]:
                if p["name"] == target_project["name"]:
                    p["path"] = str(path)
            manager._save_projects()
            
            print_result({
                "success": True,
                "project": target_project["name"],
                "ref": ref,
                "path": str(path),
                "message": f"Successfully detected and switched to project '{target_project['name']}'"
            })
        else:
            # Project found in .supabase but not in our config
            # Use CLI to get info if possible, or just add it
            manager.add_project(name=f"detected-{ref[:6]}", ref=ref, path=str(path))
            print_result({
                "success": True,
                "project": f"detected-{ref[:6]}",
                "ref": ref,
                "path": str(path),
                "message": f"Detected new project ref {ref} and added to config."
            })
            
    except Exception as e:
        print_error(str(e))


if __name__ == "__main__":
    main()
