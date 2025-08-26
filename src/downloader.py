import yt_dlp
import os

def download_video(url: str, output_path: str = "downloads/"):
    os.makedirs(output_path, exist_ok=True)
    ydl_opts = {
        'outtmpl': f'{output_path}%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        raise Exception(f"yt-dlp error: {str(e)}")