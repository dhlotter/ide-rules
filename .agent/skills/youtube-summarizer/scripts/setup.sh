#!/bin/bash
# Setup script for YouTube Summarizer skill
# Installs required Python dependencies

echo "🎬 Setting up YouTube Summarizer skill..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3 first: https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Install dependencies
echo "📦 Installing youtube-transcript-api and yt-dlp..."
pip3 install --break-system-packages youtube-transcript-api yt-dlp

if [ $? -eq 0 ]; then
    echo "✅ Setup complete! YouTube Summarizer skill is ready to use."
else
    echo "❌ Installation failed. Please check your Python/pip installation."
    exit 1
fi
