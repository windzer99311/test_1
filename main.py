# api/hls.py
import os
import tempfile
import zipfile
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import subprocess
from io import BytesIO

app = FastAPI()

@app.post("/api/hls")
async def mp3_to_hls(file: UploadFile = File(...)):
    # Make a temp directory for this request
    with tempfile.TemporaryDirectory() as tmpdir:
        mp3_path = os.path.join(tmpdir, "input.mp3")
        # Save uploaded file
        with open(mp3_path, "wb") as f:
            f.write(await file.read())

        # HLS output pattern
        segment_pattern = os.path.join(tmpdir, "seg_%03d.ts")
        playlist_path = os.path.join(tmpdir, "index.m3u8")

        # Call FFmpeg to generate HLS
        cmd = [
            "ffmpeg",
            "-y",
            "-i", mp3_path,
            "-c:a", "aac",
            "-b:a", "128k",
            "-f", "hls",
            "-hls_time", "2",
            "-hls_list_size", "0",
            "-hls_segment_filename", segment_pattern,
            playlist_path
        ]

        subprocess.run(cmd, check=True)

        # Create in-memory ZIP of .m3u8 + .ts files
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for filename in os.listdir(tmpdir):
                zipf.write(os.path.join(tmpdir, filename), arcname=filename)
        zip_buffer.seek(0)

        # Return ZIP as streaming response
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename=hls.zip"}
        )

if __name__ == "__main__":
    uvicorn.run(app)
