from fastapi import APIRouter, File, UploadFile, HTTPException
import requests
import os

router = APIRouter(prefix="/video", tags=["video"])

ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}

@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    # Validate file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Only video files are allowed.")

    # Prepare the file for sending to another API
    try:
        files = {"file": (file.filename, file.file, file.content_type)}
        url = "https://5866487b-1df3-4955-91c2-9c442416188f.mock.pstmn.io"  # Replace with your actual API URL
        response = requests.post(url, files=files)

        if response.status_code == 200:
            return {"message": "Video uploaded successfully!"}
        else:
            raise HTTPException(status_code=500, detail=f"External API error: {response.text}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")