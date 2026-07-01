import os
import uuid
import yt_dlp

DOWNLOAD_FOLDER = "downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_instagram(url):
    unique_name = str(uuid.uuid4())

    output_template = os.path.join(DOWNLOAD_FOLDER, f"{unique_name}.%(ext)s")

    ydl_opts = {
        "outtmpl": output_template,
        "quiet": True,
        "noplaylist": True,
        "merge_output_format": "mp4",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir(DOWNLOAD_FOLDER):
        if file.startswith(unique_name):
            return os.path.join(DOWNLOAD_FOLDER, file)

    return None
