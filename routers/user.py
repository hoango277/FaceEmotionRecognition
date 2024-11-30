from fastapi import APIRouter, Depends

from configs.authentication import get_current_user
from configs.database import get_db
from schemas.user import UserChange
from services.user_service import get_user_service

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@router.post("")
def change_user_info(
        user_info_change : UserChange,
        user = Depends(get_current_user),
        db = Depends(get_db),
        user_service = Depends(get_user_service),

):
    return  user_service.change_user_info(user, user_info_change, db)

@router.get("")
def get_user_info(
      cr_user = Depends(get_current_user),
        db = Depends(get_db),
        user_service = Depends(get_user_service)
):
    return user_service.get_user_info(cr_user, db)

