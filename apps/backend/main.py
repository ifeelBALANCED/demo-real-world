from fastapi import FastAPI

from api.routes import profile, user
from config import settings

# TODO: fix authorization in swagger
app = FastAPI(title=settings.app_name, version=settings.app_version)

app.include_router(user.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
