
from sqlalchemy.orm import Session


from configs.authentication import get_password_hash

from models.user import User
from schemas.base_response import BaseResponse
from schemas.user import UserChange, UserResponse


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

    def get_user_info(self, cr_user, db:Session):
        user = db.query(User).filter(User.username == cr_user.get('username')).first()
        return BaseResponse(
            data = UserResponse(
                username = user.username,
                email = user.email,
                first_name = user.first_name,
                last_name = user.last_name,
                role = user.role
            ),
            message = 'Get user info successful',
            status = 'OK'
        )