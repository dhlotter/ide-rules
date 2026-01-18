#!/usr/bin/env python3
"""
YouTube Metadata Fetcher
Fetches metadata like title and channel using yt-dlp
"""

import sys
import json
import subprocess

def get_metadata(video_id):
    """
    Get metadata for a YouTube video ID using yt-dlp
    """
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        result = subprocess.run(
            ['yt-dlp', '--dump-json', '--no-playlist', url],
            capture_output=True,
            text=True,
            check=True
        )
        metadata = json.loads(result.stdout)
        
        return {
            "success": True,
            "title": metadata.get('title'),
            "channel": metadata.get('uploader'),
            "duration": metadata.get('duration'),
            "upload_date": metadata.get('upload_date'),
            "view_count": metadata.get('view_count'),
            "description": metadata.get('description'),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"success": False, "error": "Usage: fetch_metadata.py VIDEO_ID"}))
        sys.exit(1)
    
    video_id = sys.argv[1]
    print(json.dumps(get_metadata(video_id), indent=2))
