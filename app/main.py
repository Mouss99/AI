from fastapi import FastAPI
from app.routers import video  # Import the video router

app = FastAPI()

# Include the video router
app.include_router(video.router)