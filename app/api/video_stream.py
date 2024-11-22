import asyncio
import base64

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
import cv2

video_router = APIRouter()
class VideoStream:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Cannot open camera")
            self.running = False
        else:
            self.running = True
    def get_frame(self):
        if not self.running:
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None
        _, jpeg = cv2.imencode('.jpg', frame)
        return base64.b64encode(jpeg.tobytes())
    def stop(self):
        if self.cap.isOpened():
            self.cap.release()
video_stream = VideoStream()
@video_router.websocket('/ws')
async def websocket_handler(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            frame = video_stream.get_frame()
            if frame:
                await websocket.send_json(frame)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    finally:
        video_stream.stop()
