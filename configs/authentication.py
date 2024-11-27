import os
from dotenv import load_dotenv

from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends, HTTPException

from starlette.status import HTTP_401_UNAUTHORIZED
from passlib.context import CryptContext
from fastapi.security import  OAuth2PasswordBearer
from jose import jwt, JWTError

load_dotenv()

SECRET_KEY = os.getenv("PRIVATE_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_context.hash(password)


def create_access_token(username: str, user_id: int, user_role:str ,expires_delta: timedelta):
    encode = {'sub' : username, 'id' : user_id, 'role' : user_role}
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp' : expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role : str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail= 'Cannot validate user!')
        return {'username': username, 'user_id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail= 'Cannot validate user!')




