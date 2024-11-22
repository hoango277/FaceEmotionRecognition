from fastapi import FastAPI
from app.api.auth import auth_router
from app.api.video_stream import video_router
from app.services.video_service import start_threads, stop_threads

app = FastAPI(
    title="Face Emotion Recognition",
    version="1.0.0",
)

# Đăng ký các router
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(video_router, prefix="/video", tags=["Video"])

# Khởi chạy các luồng xử lý khi ứng dụng bắt đầu
@app.on_event("startup")
async def startup():
    try:
        start_threads()
        print("Bắt đầu ứng dụng")
    except Exception as e:
        print(f"Error during startup: {e}")

# Dừng các luồng xử lý khi ứng dụng tắt
@app.on_event("shutdown")
async def shutdown():
    try:
        stop_threads()
        print("Ngắt kết nối ứng dụng")
    except Exception as e:
        print(f"Error during shutdown: {e}")

# Endpoint gốc (root)
@app.get("/")
async def root():
    return {"message": "Welcome to the Face Emotion Recognition App"}
