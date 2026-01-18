---
name: youtube-summarizer
description: Fetches YouTube video transcripts and generates comprehensive summaries
---

# YouTube Summarizer Skill

This skill enables you to fetch transcripts from YouTube videos and generate detailed summaries.

## Prerequisites

This skill requires the `youtube-transcript-api` Python package. The setup script will handle installation.

## Usage

When a user provides a YouTube URL or asks to summarize a YouTube video:

1. **Extract the Video ID**: Parse the YouTube URL to extract the video ID.
2. **Fetch Metadata**: Run the metadata fetcher to get the title, channel, and date.
   ```bash
   python3 "/Users/dhlotter/My Drive/obsidian/easyentropy/.agent/skills/youtube-summarizer/scripts/fetch_metadata.py" VIDEO_ID
   ```
3. **Fetch Transcript**: Execute the transcript fetcher script.
   ```bash
   python3 "/Users/dhlotter/My Drive/obsidian/easyentropy/.agent/skills/youtube-summarizer/scripts/fetch_transcript.py" VIDEO_ID
   ```
4. **Generate Summary**: Analyze the metadata and transcript to create a structured summary.
5. **Save to Vault**: Save the summary as a Markdown file in the specified directory.
   - **Target Directory**: `/Users/dhlotter/My Drive/obsidian/easyentropy/99-System/Attachments/Youtube-Transcripts`
   - **Filename Structure**: `YYYY-MM-DD - [Video Title] - [Video ID].md`
     - Use the upload date (YYYYMMDD) or current date.
     - Sanitize the title to remove illegal characters (e.g., `/`, `:`, `\`).

## Setup

Ensure `yt-dlp` and `youtube-transcript-api` are installed.
```bash
bash "/Users/dhlotter/My Drive/obsidian/easyentropy/.agent/skills/youtube-summarizer/scripts/setup.sh"
```

## Example Workflow

```
User: "Summarize https://www.youtube.com/watch?v=dQw4w9WgXcQ"

1. Extract video ID: dQw4w9WgXcQ
2. Fetch transcript using the script
3. Analyze the transcript content
4. Generate structured summary with key points and timestamps
5. Present to user in a clear, readable format
```

## Output Format

Present summaries in this structure:

```markdown
# 📺 [Video Title]

**Channel**: [Channel Name]
**Duration**: ~[X] minutes

## 🎯 Main Topics
- Topic 1
- Topic 2
- Topic 3

## 📝 Summary

[Detailed summary organized by topic or chronologically]

## 💡 Key Takeaways

- Takeaway 1
- Takeaway 2
- Takeaway 3

## ⏱️ Important Timestamps

- [00:00] - Introduction
- [05:30] - Key point discussed
- [12:45] - Conclusion
```
