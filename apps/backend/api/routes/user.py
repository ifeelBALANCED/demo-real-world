from typing import Optional

import cloudinary.uploader
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from api.auth import decrypt_jwt
from api.crud import user as user_crud
from api.models.user import User
from api.schemas.user import LoginUser, RegisterUser, UpdateUser
from utils import convert_bytes_to_mb

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register/")
async def register(user_data: RegisterUser):
    user = await user_crud.create_user(user_data)
    return {"email": user.email, "password": user.hashed_password}


@router.post("/login/")
async def login(user_data: LoginUser):
    token = await user_crud.verify_user_and_create_jwt(user_data)
    return {"token": token, "token_type": "bearer"}


@router.patch("/update/")
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


@router.get("/me/")
async def me(user: User = Depends(decrypt_jwt)):
    return {"email": user.email, "username": user.username, "image_url": user.image_url}
