#!/bin/bash

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKILL_DIR="$(dirname "$DIR")"

echo "Setting up Gmail Inbox Manager..."
echo "Installing Python dependencies..."

pip3 install -r "$SKILL_DIR/requirements.txt"

echo "Setup complete. Next steps:"
echo "1. Place your 'credentials.json' in: $SKILL_DIR/"
echo "2. Run the auth script: python3 $DIR/auth.py"
