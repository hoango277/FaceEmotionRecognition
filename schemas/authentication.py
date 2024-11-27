from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username : str
    user_id : str
    user_role : str

class Register(BaseModel):
    username : str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=50)
    email : str = Field(min_length=3, max_length=50)
    first_name : str = Field(min_length=1, max_length=50)
    last_name : str = Field(min_length=1, max_length=50)
    role : str = 'user'
