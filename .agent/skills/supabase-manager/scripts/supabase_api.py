#!/usr/bin/env python3
"""
Supabase API utility module
Provides common functions for interacting with Supabase projects
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import requests


class SupabaseManager:
    """Main class for managing Supabase operations"""
    
    def __init__(self, project_name: Optional[str] = None):
        self.skill_dir = Path(__file__).parent.parent
        self.projects_config_path = self.skill_dir / "projects.json"
        self.projects = self._load_projects()
        
        if project_name:
            self.active_project = self._get_project(project_name)
        else:
            self.active_project = self._get_active_project()
    
    def _load_projects(self) -> Dict:
        """Load projects configuration"""
        if not self.projects_config_path.exists():
            return {"projects": [], "active_project": None}
        
        with open(self.projects_config_path, 'r') as f:
            return json.load(f)
    
    def _save_projects(self):
        """Save projects configuration"""
        with open(self.projects_config_path, 'w') as f:
            json.dump(self.projects, f, indent=2)
    
    def _get_project(self, name: str) -> Dict:
        """Get project by name"""
        for project in self.projects.get("projects", []):
            if project["name"] == name:
                return project
        raise ValueError(f"Project '{name}' not found in configuration")
    
    def _get_active_project(self) -> Optional[Dict]:
        """Get the currently active project"""
        active_name = self.projects.get("active_project")
        if not active_name:
            if self.projects.get("projects"):
                return self.projects["projects"][0]
            return None
        return self._get_project(active_name)
    
    def add_project(self, name: str, ref: str, path: Optional[str] = None, url: Optional[str] = None):
        """Add a new project to configuration"""
        if not url:
            url = f"https://{ref}.supabase.co"
        
        project = {
            "name": name,
            "ref": ref,
            "path": path or os.getcwd(),
            "url": url,
            "active": False
        }
        
        if "projects" not in self.projects:
            self.projects["projects"] = []
        
        # Check if project already exists
        for i, p in enumerate(self.projects["projects"]):
            if p["name"] == name:
                self.projects["projects"][i] = project
                self._save_projects()
                return project
        
        self.projects["projects"].append(project)
        
        # Set as active if it's the first project
        if len(self.projects["projects"]) == 1:
            self.projects["active_project"] = name
            project["active"] = True
        
        self._save_projects()
        return project
    
    def list_projects(self) -> List[Dict]:
        """List all configured projects"""
        return self.projects.get("projects", [])
    
    def switch_project(self, name: str):
        """Switch active project"""
        project = self._get_project(name)
        
        # Update active flags
        for p in self.projects["projects"]:
            p["active"] = (p["name"] == name)
        
        self.projects["active_project"] = name
        self._save_projects()
        self.active_project = project
        return project
    
    def run_cli_command(self, command: List[str], cwd: Optional[str] = None) -> Dict[str, Any]:
        """Run a Supabase CLI command"""
        if not cwd and self.active_project:
            cwd = self.active_project.get("path", os.getcwd())
        
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True
            )
            return {
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "stdout": e.stdout,
                "stderr": e.stderr,
                "returncode": e.returncode,
                "error": str(e)
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Supabase CLI not found. Please install it: brew install supabase/tap/supabase"
            }
    
    def execute_sql(self, query: str, project_name: Optional[str] = None) -> Dict[str, Any]:
        """Execute SQL query via Supabase CLI"""
        if project_name:
            original_project = self.active_project
            self.switch_project(project_name)
        
        # Write query to temp file
        temp_query_file = self.skill_dir / "temp_query.sql"
        with open(temp_query_file, 'w') as f:
            f.write(query)
        
        try:
            result = self.run_cli_command([
                "supabase", "db", "query",
                "--file", str(temp_query_file)
            ])
            
            if result["success"]:
                result["query"] = query
            
            return result
        finally:
            # Clean up temp file
            if temp_query_file.exists():
                temp_query_file.unlink()
            
            # Restore original project if we switched
            if project_name and original_project:
                self.switch_project(original_project["name"])
    
    def get_project_status(self, project_name: Optional[str] = None) -> Dict[str, Any]:
        """Get comprehensive project status"""
        if project_name:
            original_project = self.active_project
            self.switch_project(project_name)
        
        try:
            result = self.run_cli_command(["supabase", "status"])
            
            status = {
                "project": self.active_project,
                "cli_output": result.get("stdout", ""),
                "success": result["success"]
            }
            
            if not result["success"]:
                status["error"] = result.get("error", result.get("stderr", "Unknown error"))
            
            return status
        finally:
            if project_name and original_project:
                self.switch_project(original_project["name"])
    
    def list_migrations(self, project_name: Optional[str] = None) -> Dict[str, Any]:
        """List all migrations"""
        if project_name:
            original_project = self.active_project
            self.switch_project(project_name)
        
        try:
            result = self.run_cli_command(["supabase", "migration", "list"])
            
            migrations = {
                "project": self.active_project,
                "migrations": [],
                "success": result["success"]
            }
            
            if result["success"]:
                # Parse migration list from output
                lines = result["stdout"].strip().split('\n')
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        migrations["migrations"].append(line.strip())
            else:
                migrations["error"] = result.get("error", result.get("stderr", "Unknown error"))
            
            return migrations
        finally:
            if project_name and original_project:
                self.switch_project(original_project["name"])
    
    def create_migration(self, name: str, project_name: Optional[str] = None) -> Dict[str, Any]:
        """Create a new migration"""
        if project_name:
            original_project = self.active_project
            self.switch_project(project_name)
        
        try:
            result = self.run_cli_command([
                "supabase", "migration", "new", name
            ])
            
            migration = {
                "project": self.active_project,
                "name": name,
                "success": result["success"]
            }
            
            if result["success"]:
                migration["output"] = result["stdout"]
            else:
                migration["error"] = result.get("error", result.get("stderr", "Unknown error"))
            
            return migration
        finally:
            if project_name and original_project:
                self.switch_project(original_project["name"])
    
    def apply_migrations(self, project_name: Optional[str] = None) -> Dict[str, Any]:
        """Apply pending migrations"""
        if project_name:
            original_project = self.active_project
            self.switch_project(project_name)
        
        try:
            result = self.run_cli_command(["supabase", "db", "push"])
            
            apply_result = {
                "project": self.active_project,
                "success": result["success"]
            }
            
            if result["success"]:
                apply_result["output"] = result["stdout"]
            else:
                apply_result["error"] = result.get("error", result.get("stderr", "Unknown error"))
            
            return apply_result
        finally:
            if project_name and original_project:
                self.switch_project(original_project["name"])
    
    def get_logs(self, log_type: str = "all", hours: int = 1, project_name: Optional[str] = None) -> Dict[str, Any]:
        """Get logs from Supabase"""
        if project_name:
            original_project = self.active_project
            self.switch_project(project_name)
        
        try:
            # Supabase CLI logs command
            cmd = ["supabase", "logs"]
            
            if log_type != "all":
                cmd.extend(["--type", log_type])
            
            result = self.run_cli_command(cmd)
            
            logs = {
                "project": self.active_project,
                "type": log_type,
                "hours": hours,
                "success": result["success"]
            }
            
            if result["success"]:
                logs["logs"] = result["stdout"]
            else:
                logs["error"] = result.get("error", result.get("stderr", "Unknown error"))
            
            return logs
        finally:
            if project_name and original_project:
                self.switch_project(original_project["name"])


def format_output(data: Any, format_type: str = "json") -> str:
    """Format output data"""
    if format_type == "json":
        return json.dumps(data, indent=2)
    elif format_type == "table":
        try:
            from tabulate import tabulate
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                return tabulate(data, headers="keys", tablefmt="grid")
            return str(data)
        except ImportError:
            return json.dumps(data, indent=2)
    else:
        return str(data)


def print_result(result: Dict[str, Any], format_type: str = "json"):
    """Print result to stdout"""
    print(format_output(result, format_type))


def print_error(error: str):
    """Print error to stderr"""
    print(f"ERROR: {error}", file=sys.stderr)
    sys.exit(1)
