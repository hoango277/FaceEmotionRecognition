import queue

from fastapi import APIRouter
from threading import Thread

from app.services.camera_thread import CameraThread, DetectionThread

video_router = APIRouter()

@video_router.get("/start")
async def start_video_stream():
    frame_queue = queue.Queue(maxsize=1)
    result_queue = queue.Queue(maxsize=1)

    camera_thread = CameraThread(frame_queue, result_queue)
    detection_thread = DetectionThread(frame_queue, result_queue)

    camera_thread.start()
    detection_thread.start()

    return {"message": "Video streaming started!"}

@video_router.get("/stop")
async def stop_video_stream():
    return {"message": "Video streaming stopped!"}
