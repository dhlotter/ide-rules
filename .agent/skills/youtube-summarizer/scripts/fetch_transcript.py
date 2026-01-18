#!/usr/bin/env python3
"""
YouTube Transcript Fetcher
Fetches transcripts from YouTube videos using youtube-transcript-api
"""

import sys
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

def fetch_transcript(video_id):
    """
    Fetch transcript for a given YouTube video ID
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        dict: Transcript data with metadata
    """
    try:
        # Create API instance
        api = YouTubeTranscriptApi()
        
        # Try to fetch the transcript (will try English by default)
        try:
            fetched_transcript = api.fetch(video_id, languages=['en'])
        except Exception as e:
            # If English fails, try without language specification
            fetched_transcript = api.fetch(video_id)
        
        # Convert snippets to dictionary format
        transcript_data = []
        for snippet in fetched_transcript.snippets:
            transcript_data.append({
                'text': snippet.text,
                'start': snippet.start,
                'duration': snippet.duration
            })
        
        # Calculate total duration
        if transcript_data:
            last_snippet = transcript_data[-1]
            total_duration = last_snippet['start'] + last_snippet['duration']
        else:
            total_duration = 0
        
        # Determine transcript type
        transcript_type = "auto-generated" if fetched_transcript.is_generated else "manual"
        
        # Format the output
        result = {
            "success": True,
            "video_id": video_id,
            "transcript_type": transcript_type,
            "language": fetched_transcript.language,
            "language_code": fetched_transcript.language_code,
            "duration_seconds": total_duration,
            "transcript": transcript_data
        }
        
        return result
        
    except TranscriptsDisabled:
        return {
            "success": False,
            "error": "Transcripts are disabled for this video",
            "video_id": video_id
        }
    except NoTranscriptFound:
        return {
            "success": False,
            "error": "No transcript found for this video",
            "video_id": video_id
        }
    except VideoUnavailable:
        return {
            "success": False,
            "error": "Video is unavailable or does not exist",
            "video_id": video_id
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "video_id": video_id
        }

def format_timestamp(seconds):
    """Convert seconds to MM:SS or HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"

def main():
    if len(sys.argv) != 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: fetch_transcript.py VIDEO_ID"
        }))
        sys.exit(1)
    
    video_id = sys.argv[1]
    result = fetch_transcript(video_id)
    
    # Add formatted timestamps to transcript entries
    if result.get("success") and result.get("transcript"):
        for entry in result["transcript"]:
            entry["formatted_time"] = format_timestamp(entry["start"])
    
    # Output as JSON
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
