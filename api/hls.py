import os
import shutil
import subprocess
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

app = FastAPI()

FFMPEG_PATH = "/var/task/api/bin/ffmpeg"

@app.post("/api/hls")
async def mp3_to_hls(file: UploadFile = File(...)):
    if not file.filename.endswith(".mp3"):
        return {"error": "Only MP3 files allowed"}

    with tempfile.TemporaryDirectory() as tmp:
        mp3_path = os.path.join(tmp, "input.mp3")
        with open(mp3_path, "wb") as f:
            f.write(await file.read())

        hls_dir = os.path.join(tmp, "hls")
        os.makedirs(hls_dir)

        playlist = os.path.join(hls_dir, "playlist.m3u8")
        segments = os.path.join(hls_dir, "segment_%03d.ts")

        cmd = [
            FFMPEG_PATH,
            "-y",
            "-i", mp3_path,
            "-c:a", "aac",
            "-b:a", "128k",
            "-f", "hls",
            "-hls_time", "2",
            "-hls_list_size", "0",
            "-hls_segment_filename", segments,
            playlist,
        ]

        subprocess.run(cmd, check=True)

        zip_path = os.path.join(tmp, "hls.zip")
        shutil.make_archive(zip_path.replace(".zip", ""), "zip", hls_dir)

        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename="audio_hls.zip"
        )
