from fastapi import FastAPI

from services.video_service import  VideoService

app = FastAPI()


video_service = VideoService()
@app.get("/stream")
def get_video():
    return video_service.get_video()

@app.get("/stop")
def stop_video():
    video_service.stop_video()
    return {"message": "Đã tắt stream"}