from fastapi import FastAPI

from api.routes import user
from config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.include_router(user.router, prefix="/api")
