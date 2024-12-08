# download_video.py
import yt_dlp


def download_video(search_query):
    ydl_opts = {
        "format": "best",
        "outtmpl": "video.mp4",  # save the video to a file
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch:{search_query}"])
    return "video.mp4" 
