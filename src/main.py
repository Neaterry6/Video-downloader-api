from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from downloader import download_video
import os
import re

app = FastAPI(title="Video Downloader API")

@app.get("/download")
async def download(url: str):
    if not re.match(r'^https?://', url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    try:
        file_path = download_video(url)
        return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type="video/mp4")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
