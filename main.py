from fastapi import FastAPI
import subprocess,uvicorn
input_file="song.mp3"
app = FastAPI()
@app.get("/half")
def half():
    result = subprocess.run(
        [
            "ffprobe",
            "-i", input_file,
            "-show_entries", "format=duration",
            "-v", "quiet",
            "-of", "csv=p=0"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print(result.stdout)
    print(result.stderr)
if __name__ == "__main__":
    uvicorn.run(app)
