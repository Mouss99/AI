from fastapi import FastAPI, File, UploadFile, HTTPException
import requests
import os

app = FastAPI()

# External API URL (replace with your actual API URL)
EXTERNAL_API_URL = "https://5866487b-1df3-4955-91c2-9c442416188f.mock.pstmn.io"

# Allowed video file extensions
ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    """
    Endpoint to upload a video file.
    - Accepts a video file.
    - Validates the file type.
    - Sends the file to an external API.
    """
    # Validate file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only video files are allowed."
        )

    try:
        # Prepare the file for sending to the external API
        files = {"file": (file.filename, file.file, file.content_type)}

        # Send the file to the external API
        response = requests.post(EXTERNAL_API_URL, files=files)

        # Check if the external API responded successfully
        if response.status_code == 200:
            return {"message": "Video uploaded successfully!"}
        else:
            raise HTTPException(
                status_code=500,
                detail=f"External API error: {response.text}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )