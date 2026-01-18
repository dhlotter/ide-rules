---
name: audio-transcriber
description: Transcribes and translates audio files to English, producing a full transcript and a summary.
---

# Audio Transcriber Skill

This skill allows you to transcribe audio files and translate them into English. It generates both a full text transcription and a summarized overview of the content.

## Prerequisites
- Python 3
- `openai-whisper` package
- `ffmpeg` (must be installed on the system)

## Usage

### 1. Gather Information
Before running the transcription, ensure you have the following three items. **If any are missing, you MUST prompt the user for them:**
1.  **Input File**: The absolute path to the audio file (e.g., `.mp3`, `.m4a`, `.wav`).
2.  **Output Directory**: The folder where the results should be saved.
3.  **Input Language**: The language spoken in the audio (e.g., "Afrikaans", "French"). If unknown, ask the user or use "auto" to let the model detect it.

### 2. Execution
Run the transcription (ensure task is set to `translate` to output English):

```bash
python3 "/Users/dhlotter/My Drive/obsidian/easyentropy/.agent/skills/audio-transcriber/scripts/transcribe.py" --file "[INPUT_FILE]" --output "[OUTPUT_DIR]" --language "[LANGUAGE]"
```

### 3. Post-Processing
The script will output the raw transcription text to the terminal and save a `.txt` file in the directory.
**You (the Agent) must then:**
1.  Read the transcription output.
2.  Generate a **Summary** of the audio content.
3.  Save the summary as a Markdown file (e.g., `[Filename]_Summary.md`) in the **Output Directory**.

### Summary Format
The summary file should contain:
-   **Metadata**: Original filename, Date, Detected/Provided Language.
-   **Executive Summary**: A concise paragraph describing the main topic.
-   **Key Points**: Bullet points of essential information.
-   **Action Items**: (If applicable) Any tasks or follow-ups mentioned.

## Setup
If dependencies are missing, run:
```bash
bash "/Users/dhlotter/My Drive/obsidian/easyentropy/.agent/skills/audio-transcriber/scripts/setup.sh"
```
