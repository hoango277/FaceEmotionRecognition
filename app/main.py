from fastapi import FastAPI
from app.api.auth import auth_router
from app.api.video_stream import video_router
from app.services.video_service import start_threads, stop_threads

# Tạo ứng dụng FastAPI
app = FastAPI(
    title="Face Emotion Recognition API",
    description="API for user authentication and video streaming for emotion recognition.",
    version="1.0.0"
)

# Đăng ký các router
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(video_router, prefix="/video", tags=["Video Stream"])

# Hàm khởi động và tắt ứng dụng
async def startup_event():
    """
    Hàm xử lý khi ứng dụng khởi động.
    Gọi các tiến trình cần thiết (nếu có).
    """
    start_threads()

async def shutdown_event():
    """
    Hàm xử lý khi ứng dụng tắt.
    Dừng các tiến trình hoặc giải phóng tài nguyên.
    """
    stop_threads()

# Tích hợp các hàm khởi động/tắt ứng dụng vào lifecycle của FastAPI
@app.on_event("startup")
async def custom_startup():
    await startup_event()

@app.on_event("shutdown")
async def custom_shutdown():
    await shutdown_event()

# Endpoint mặc định
@app.get("/")
async def root():
    """
    Endpoint chính, trả về thông báo chào mừng.
    """
    return {"message": "Welcome to the Face Emotion Recognition API"}
