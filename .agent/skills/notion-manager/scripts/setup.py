#!/usr/bin/env python3
"""
Setup script for Notion Manager skill.
Prompts user for Notion integration token and saves it securely.
"""

import os
import sys
from pathlib import Path

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.parent
    token_file = script_dir / "token.txt"
    
    print("=" * 60)
    print("Notion Manager Setup")
    print("=" * 60)
    print("\nYou need a Notion integration token to use this skill.")
    print("To get one:")
    print("1. Go to https://www.notion.so/my-integrations")
    print("2. Click '+ New integration'")
    print("3. Name it (e.g., 'Obsidian Agent')")
    print("4. Copy the 'Internal Integration Token'")
    print("5. Share the pages/databases you want to access with this integration")
    print("\n" + "=" * 60 + "\n")
    
    # Check if token already exists
    if token_file.exists():
        print(f"⚠️  Token file already exists at: {token_file}")
        response = input("Do you want to replace it? (y/N): ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            return 0
    
    # Get the token from user
    token = input("\nEnter your Notion integration token: ").strip()
    
    if not token:
        print("❌ Error: No token provided.")
        return 1
    
    if not (token.startswith("secret_") or token.startswith("ntn_")):
        print("⚠️  Warning: Notion integration tokens usually start with 'secret_' or 'ntn_'")
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            return 0
    
    # Save the token
    try:
        token_file.write_text(token)
        # Set restrictive permissions (owner read/write only)
        os.chmod(token_file, 0o600)
        print(f"\n✅ Token saved successfully to: {token_file}")
        print("✅ File permissions set to owner read/write only")
        print("\n🎉 Setup complete! You can now use the Notion Manager skill.")
        return 0
    except Exception as e:
        print(f"\n❌ Error saving token: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
