from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import yt_dlp
import os
import base64
import tempfile
import logging

app = FastAPI()

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/download")
async def download_video(url: str):
    # Decode cookies from environment variable
    cookies_b64 = os.environ.get("COOKIES_B64")
    if not cookies_b64:
        raise HTTPException(status_code=500, detail="COOKIES_B64 environment variable not set")

    try:
        cookies_content = base64.b64decode(cookies_b64).decode("utf-8")
    except Exception as e:
        logger.error(f"Failed to decode cookies: {str(e)}")
        raise HTTPException(status_code=500, detail="Invalid COOKIES_B64 format")

    # Write cookies to a temporary file
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as tmp:
        tmp.write(cookies_content)
        cookiefile = tmp.name

    ydl_opts = {
        "cookiefile": cookiefile,
        "quiet": True,
        "no_warnings": True,
        "format": "bestvideo+bestaudio/best",  # Attempts to merge best video and audio
        "outtmpl": "%(id)s.%(ext)s",  # Save with video ID as filename
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info to get filename
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            # Download the video
            ydl.download([url])
            if not os.path.exists(filename):
                raise HTTPException(status_code=500, detail="Download failed: File not found")
            return FileResponse(
                path=filename,
                media_type="video/mp4",
                filename=f"{info['id']}.{info.get('ext', 'mp4')}"
            )
    except Exception as e:
        logger.error(f"yt-dlp error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
    finally:
        # Clean up temporary files
        try:
            os.unlink(cookiefile)
            if os.path.exists(filename):
                os.unlink(filename)
        except Exception as e:
            logger.warning(f"Cleanup(cleanup failed: {str(e)}")