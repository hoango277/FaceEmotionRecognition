
from fastapi import APIRouter, Request, Depends

from configs.database import get_db

from schemas.email import EmailSchema
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


@router.get("/reset")
async def reset_password_email(
        req : Request,
        db = Depends(get_db),
        mail_service = Depends(get_mail_service)
):
    return await mail_service.reset_password(req, db)
