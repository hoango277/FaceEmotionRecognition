from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import User
from app.db.schemas import UserCreate, UserLogin

# Cấu hình mã hóa mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Thông tin JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Hàm tạo JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Tạo một JWT token với dữ liệu và thời gian hết hạn"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class AuthService:
    @staticmethod
    def get_db():
        """Quản lý kết nối cơ sở dữ liệu"""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    def register_user(user: UserCreate):
        """Đăng ký người dùng mới"""
        db: Session = next(AuthService.get_db())
        # Mã hóa mật khẩu người dùng
        hashed_password = pwd_context.hash(user.password)
        # Tạo bản ghi người dùng mới
        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            role=user.role,
            created_at=datetime.utcnow()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def login_user(user: UserLogin) -> Optional[str]:
        """Đăng nhập người dùng và tạo JWT token"""
        db: Session = next(AuthService.get_db())
        # Tìm người dùng trong CSDL theo username
        db_user = db.query(User).filter(User.username == user.username).first()
        if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
            return None  # Sai tên đăng nhập hoặc mật khẩu

        # Tạo token truy cập nếu đăng nhập thành công
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.username}, expires_delta=access_token_expires
        )
        return access_token

    @staticmethod
    def reset_password(email: str) -> bool:
        """Xử lý quên mật khẩu"""
        db: Session = next(AuthService.get_db())
        # Kiểm tra email trong CSDL
        db_user = db.query(User).filter(User.email == email).first()
        if not db_user:
            return False  # Không tìm thấy email

        # Logic gửi email đặt lại mật khẩu (giả định đã gửi thành công)
        # Thực tế có thể sử dụng SMTP hoặc tích hợp dịch vụ gửi email
        return True
