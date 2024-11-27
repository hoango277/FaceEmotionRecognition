from fastapi import APIRouter, Depends

from configs.authentication import get_current_user

router = APIRouter(
    prefix="/api",
    tags=["video"],
)

from services.video_service import VideoService

video_service = VideoService()
@router.get("/stream")
def get_video(user = Depends(get_current_user)):
    return video_service.get_video(user)

@router.get("/stop")
def stop_video(user = Depends(get_current_user)):
    video_service.stop_video(user)
    return {"message": "Đã tắt stream"}