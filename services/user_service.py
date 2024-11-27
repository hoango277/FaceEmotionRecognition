from sqlalchemy.orm import Session
from ultralytics.data.utils import get_hash

from configs.authentication import get_password_hash
from exception import raise_error
from models.user import User
from schemas.base_response import BaseResponse
from schemas.user import UserChange


def get_user_service():
    try:
        yield UserService()
    finally:
        pass

class UserService:
    def change_user_info(self, user, user_info_change: UserChange, db:Session):
        user_to_change = db.query(User).filter(User.username == user.get('username')).first()
        mail_check = db.query(User).filter(User.email == user_info_change.email).first()
        if mail_check.username != user_to_change.username:
            return BaseResponse(
                message='Email already registered',
                status = 'error'
            )

        user_to_change.hashed_password = get_password_hash(user_info_change.password)
        user_to_change.email = user_info_change.email
        user_to_change.first_name = user_info_change.first_name
        user_to_change.last_name = user_info_change.last_name
        db.add(user_to_change)
        db.commit()

        return BaseResponse(
            message='User info changed',
            status = 'OK'
        )