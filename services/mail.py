from fastapi.params import Query
from fastapi_mail import MessageSchema, MessageType, FastMail
from starlette.requests import Request
from starlette.responses import JSONResponse

from configs.ConnectionConfig import conf
from configs.authentication import get_password_hash
from exception import raise_error
from models.user import User
from schemas import email
from schemas.base_response import BaseResponse
from schemas.user import PasswordReset


def get_mail_service():
    try:
        yield MailService()
    finally:
        pass


html = """
<p>Hi,</p>
<p>Click vào link bên dưới để reset password của bạn:</p>
<p><a href="{reset_link}">Reset Password</a></p>
"""

class MailService:
    async def send_reset_password_mail(self, email):
        reset_link = f"http://127.0.0.1:8000/api/reset?email={email.email}"
        body = html.format(reset_link=reset_link)

        # Send the email with FastMail
        message = MessageSchema(
            subject="Reset Password",
            recipients=[email.email],
            body=body,
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message)

        return BaseResponse(
            message="Email sent successfully!",
            status = "OK"
        )

    async def reset_password(self, request : Request, db, new_password: PasswordReset):
        email_set = request.query_params.get("email")
        email_check = db.query(User).filter(User.email == email_set).first()

        if email_check is None:
            return raise_error(100009)
        if new_password.new_password != new_password.confirm_password:
            return BaseResponse(
                message="Passwords do not match!",
                status = "OK"
            )

        email_check.hashed_password = get_password_hash(new_password.new_password)
        db.add(email_check)
        db.commit()

        return BaseResponse(
            message="Password updated successfully!",
            status = "OK"
        )




