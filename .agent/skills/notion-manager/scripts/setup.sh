#!/bin/bash
# Setup script for Notion Manager skill

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Setting up Notion Manager skill..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv "$SKILL_DIR/venv"

# Activate virtual environment
source "$SKILL_DIR/venv/bin/activate"

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r "$SKILL_DIR/requirements.txt"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Run the authentication script to save your Notion token:"
echo "   \"$SKILL_DIR/venv/bin/python\" \"$SKILL_DIR/scripts/setup.py\""
echo ""
echo "2. Test the connection by listing databases:"
echo "   \"$SKILL_DIR/venv/bin/python\" \"$SKILL_DIR/scripts/list_databases.py\""
