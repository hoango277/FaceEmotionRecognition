from typing import TypeVar, Optional

from pydantic import BaseModel

T = TypeVar('T')
class BaseResponse(BaseModel):
    data: Optional[T] = None
    message: str = ''
    status: str = "success"