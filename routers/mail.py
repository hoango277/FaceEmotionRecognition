
from fastapi import APIRouter, Request, Depends

from configs.database import get_db
from schemas import email
from schemas.email import EmailSchema
from schemas.user import PasswordRequest, PasswordReset
from services.mail import get_mail_service

router = APIRouter(
    prefix="/api",
    tags=["email"],
)



@router.post("/email")
async def send_reset_password_mail(
        email: EmailSchema,
        mail_service = Depends(get_mail_service),
) :
    return await mail_service.send_reset_password_mail(email)


@router.post("/reset")
async def reset_password_email(
        new_password : PasswordReset,
        req : Request,
        db = Depends(get_db),
        mail_service = Depends(get_mail_service)
):
    return await mail_service.reset_password(req, db, new_password)
