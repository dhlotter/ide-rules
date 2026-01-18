#!/bin/bash
# Setup script for Audio Transcriber skill

echo "🎙️ Setting up Audio Transcriber skill..."

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    exit 1
fi

# Check for FFmpeg (Required by Whisper)
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg is missing!"
    echo "   Please install it using Homebrew: 'brew install ffmpeg'"
    # We don't exit here, but the script might fail later without it.
else
    echo "✓ FFmpeg found"
fi

# Install Python dependencies
echo "📦 Installing openai-whisper..."
pip3 install --break-system-packages openai-whisper

if [ $? -eq 0 ]; then
    echo "✅ Setup complete! Audio Transcriber is ready."
else
    echo "❌ Installation failed."
    exit 1
fi
