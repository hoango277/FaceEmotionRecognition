from fastapi import APIRouter, HTTPException, Depends
from app.db.schemas import UserCreate, UserLogin
from app.services.auth_services import AuthService

auth_router = APIRouter()

@auth_router.post("/register")
async def register(user: UserCreate):
    result = await AuthService.register_user(user)
    if not result:
        raise HTTPException(status_code=400, detail="Đăng ký không thành công")
    return {"message": "Đăng ký thành công."}

@auth_router.post("/login")
async def login(user: UserLogin):
    token = await AuthService.login_user(user)
    if not token:
        raise HTTPException(status_code=401, detail="Kiểm tra lại tên người dùng hoặc mật khẩu.")
    return {"access_token": token, "token_type": "bearer"}

@auth_router.post("/forgot-password")
async def forgot_password(email: str):
    success = await AuthService.reset_password(email)
    if not success:
        raise HTTPException(status_code=404, detail="Email not found.")
    return {"message": "Mã đã được gửi tới Email."}
