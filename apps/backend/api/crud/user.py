from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, status

from api.auth import create_jwt
from api.exceptions import RecordNotFound
from api.models import User
from api.schemas.user import LoginUser, RegisterUser, UpdateUser

ph = PasswordHasher()


async def create_user(user_data: RegisterUser) -> User:
    user = await User.filter(email=user_data.email, password=user_data.password)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    hashed_password = ph.hash(user_data.password)
    user = await User.create(email=user_data.email, username=user_data.username, hashed_password=hashed_password)
    return user


# TODO: temp fix
async def update_user(user_data: UpdateUser, image_url: str, user: User) -> User:
    if user_data:
        if user_data.password:
            await user.update(hashed_password=ph.hash(user_data.password))
        if user_data.username:
            await user.update(username=user_data.username)
    if image_url:
        await user.update(image_url=image_url)
    return user


async def verify_user_and_create_jwt(user_data: LoginUser) -> bool:
    try:
        user = await User.get(email=user_data.email)
        ph.verify(user.hashed_password, user_data.password)

        token = create_jwt(user)
    except (RecordNotFound, VerifyMismatchError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user credentials!")

    return token
