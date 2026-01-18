#!/usr/bin/env python3
"""
Audio Transcriber & Translator
Uses OpenAI Whisper to transcribe audio and translate it to English.
"""

import argparse
import sys
import os
import warnings
import whisper

# Suppress warnings
warnings.filterwarnings("ignore")

def transcribe_audio(file_path, output_dir, language):
    print(f"🎧 Loading Whisper model (this may take a moment)...")
    # Load the base model - good balance of speed and accuracy for general use
    model = whisper.load_model("base")

    print(f"🔄 Transcribing and translating '{os.path.basename(file_path)}'...")
    
    # Set options
    options = {"task": "translate"} # Always translate to English
    if language and language.lower() != "auto":
        options["language"] = language

    # Run transcription
    result = model.transcribe(file_path, **options)
    text = result["text"].strip()

    # Prepare output filenames
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    txt_path = os.path.join(output_dir, f"{base_name}_transcript.txt")

    # Save full transcript
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"✅ Transcription saved to: {txt_path}")
    print("\n--- TRANSCRIPT START ---")
    print(text)
    print("--- TRANSCRIPT END ---\n")

def main():
    parser = argparse.ArgumentParser(description="Transcribe and translate audio to English.")
    parser.add_argument("--file", required=True, help="Path to the input audio file")
    parser.add_argument("--output", required=True, help="Directory to save the output")
    parser.add_argument("--language", default="auto", help="Input language (default: auto)")

    args = parser.parse_args()

    # Validation
    if not os.path.exists(args.file):
        print(f"❌ Error: Input file not found: {args.file}")
        sys.exit(1)
    
    if not os.path.exists(args.output):
        try:
            os.makedirs(args.output)
            print(f"📁 Created output directory: {args.output}")
        except OSError as e:
            print(f"❌ Error creating output directory: {e}")
            sys.exit(1)

    transcribe_audio(args.file, args.output, args.language)

if __name__ == "__main__":
    main()
