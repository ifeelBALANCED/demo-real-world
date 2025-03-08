from fastapi import HTTPException, status

from api.exceptions import RecordNotFound
from api.models import User


# TODO: maybe rewrite it later with some switch to determine whether follow or unfollow?
async def follow_user(username: str, request_user: User) -> User:
    try:
        user_to_follow = await User.get(username=username)
    except RecordNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await request_user.following.add(user_to_follow)
    return request_user


async def unfollow_user(username: str, request_user: User) -> User:
    try:
        user_to_unfollow = await User.get(username=username)
    except RecordNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await request_user.following.remove(user_to_unfollow)
    return request_user


async def get_profiles() -> list[User]:
    profiles = await User.all()
    return profiles
