from fastapi.params import Query
from fastapi_mail import MessageSchema, MessageType, FastMail
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse

from configs.ConnectionConfig import conf
from configs.authentication import get_password_hash
from exception import raise_error
from models.user import User

from schemas.base_response import BaseResponse



def get_mail_service():
    try:
        yield MailService()
    finally:
        pass


html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
</head>
<body>
    <p>Hi,</p>
    <p>Click vào link bên dưới để reset password của bạn:</p>
    <p>
        <a href="{reset_link}">Reset Password</a>
    </p>
    <p>Mật khẩu của bạn sẽ được reset thành: <strong>12345678</strong></p>
    <p>Chúc bạn một ngày tốt lành!</p>
</body>
</html>
"""

class MailService:
    async def send_reset_password_mail(self, email):
        reset_link = f"http://127.0.0.1:8000/api/reset?email={email.email}"

        body = html.format(reset_link=reset_link)

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

    async def reset_password(self, request : Request, db):
        email_set = request.query_params.get("email")
        email_check = db.query(User).filter(User.email == email_set).first()

        if email_check is None:
            return raise_error(100009)


        email_check.hashed_password = get_password_hash("12345678")
        db.add(email_check)
        db.commit()

        return HTMLResponse(
            content=(
                "Password updated successfully!<br>"
                f"Your username is {email_check.username}<br>"
                "Your new password is 12345678"
            ),
            status_code=200
        )





