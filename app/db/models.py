from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Float
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(250), unique=True, index=True)
    email = Column(String(250), unique=True, index=True)
    hashed_password = Column(String(50))
    role = Column(String(50))
    created_at = Column(TIMESTAMP)
    emotion_histories = relationship("EmotionHistory", back_populates="user")
    user_sessions = relationship("UserSession", back_populates="user")  # Sửa từ user_Sessions thành user_sessions
    images = relationship("Image", back_populates="user")

class UserSession(Base):
    __tablename__ = 'user_session'  # Bảng user_session
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    session_token = Column(String(255))
    ip_address = Column(String(100))
    device = Column(String(100))
    created_at = Column(TIMESTAMP)
    last_accessed_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="user_sessions")
