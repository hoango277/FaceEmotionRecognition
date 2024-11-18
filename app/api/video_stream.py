from fastapi import APIRouter, HTTPException
import cv2
import time

from starlette.responses import StreamingResponse

video_router = APIRouter()


# Generator function to yield frames
def video_generator():
    cap = cv2.VideoCapture(0)  # Open the default camera (0)

    if not cap.isOpened():
        raise HTTPException(status_code=500, detail="Cannot access the camera.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue

            # Yield the frame as byte stream
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

            time.sleep(0.03)  # Control the frame rate (approx. 30 FPS)
    finally:
        cap.release()  # Release the video capture when done


# FastAPI route to stream video
@video_router.get("/stream")
async def stream_video():
    return StreamingResponse(video_generator(), media_type="multipart/x-mixed-replace; boundary=frame")
