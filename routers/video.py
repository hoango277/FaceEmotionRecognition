from fastapi import APIRouter, Depends

from configs.authentication import get_current_user

router = APIRouter(
    prefix="/api",
    tags=["video"],
)

from services.video_service import VideoService

video_service = VideoService()
@router.get("/stream")
def get_video():
    return video_service.get_video()

@router.get("/stop")
def stop_video():
    video_service.stop_video()
    return {"message": "Đã tắt stream"}