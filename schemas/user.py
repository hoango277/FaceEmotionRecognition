from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str  = Field(min_length=8, max_length=30)
    email: str = Field(min_length=3, max_length=30)
    first_name: str = Field(min_length=3, max_length=30)
    last_name: str = Field(min_length=3, max_length=30)
    role: str = Field(min_length=3, max_length=30)

    class Config:
        from_attributes = True

class PasswordRequest(BaseModel):
    old_password: str = Field(min_length=8, max_length=30)
    new_password: str = Field(min_length=8, max_length=30)