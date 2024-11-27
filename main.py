from fastapi import FastAPI

from routers.video import router as video_router
from routers.authentication import router as authentication_router
from routers.mail import router as mail_router
from routers.user import router as user_router

app = FastAPI()

app.include_router(video_router)
app.include_router(authentication_router)

app.include_router(mail_router)
app.include_router(user_router)
