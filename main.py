from fastapi import FastAPI

from routers.video import router as video_router
from routers.authentication import router as authentication_router

app = FastAPI()

app.include_router(video_router)
app.include_router(authentication_router)

