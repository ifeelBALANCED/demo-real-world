from typing import Optional

import cloudinary.uploader
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile

from api.auth import decrypt_jwt
from api.crud import user as user_crud
from api.models import User
from api.schemas.user import LoginUser, RegisterUser, UpdateUser
from config import settings
from utils import convert_bytes_to_mb

app = FastAPI()
cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
)


@app.post("/register/")
async def register(user_data: RegisterUser):
    user = await user_crud.create_user(user_data)
    return {"email": user.email, "password": user.hashed_password}


@app.post("/login/")
async def login(user_data: LoginUser):
    token = await user_crud.verify_user_and_create_jwt(user_data)
    return {"token": token, "token_type": "bearer"}


@app.patch("/update/")
async def update(
    user_data: UpdateUser = None, user: User = Depends(decrypt_jwt), file: Optional[UploadFile] = File(None)
):
    if not file:
        raise HTTPException(
            status_code=400,
            detail="No file provided",
        )
    file_size = convert_bytes_to_mb(file.size)
    if file_size > 2.0:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 2 MB limit",
        )

    result = cloudinary.uploader.upload(file.file)
    image_url = result["secure_url"]
    user = await user_crud.update_user(user_data, image_url, user)
    return {"email": user.email, "username": user.username, "image_url": user.image_url}


@app.get("/me/")
async def me(user: User = Depends(decrypt_jwt)):
    return {"email": user.email, "username": user.username, "image_url": user.image_url}
