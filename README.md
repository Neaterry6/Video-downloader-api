# Video Downloader API

A FastAPI-based API to download videos using yt-dlp.

## Setup
1. Clone repo: `https://github.com/Neaterry6/Video-downloader-api.git`
2. Create venv: `python -m venv venv`
3. Activate venv: `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)
4. Install deps: `pip install -r requirements.txt`
5. Run: `uvicorn src.main:app --reload`

## Usage
`curl "http://localhost:8000/download?url=https://www.youtube.com/watch?v=example"`

## Notes
- Supports yt-dlp-compatible platforms.
- Ensure compliance with platform terms and copyright laws.
