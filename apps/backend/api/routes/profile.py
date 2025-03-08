from fastapi import APIRouter, Depends, status

from api.auth import decrypt_jwt
from api.crud import profile as profile_crud
from api.models.user import User
from api.schemas.profile import ProfileDetail, ProfileList

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("/", response_model=ProfileList)
async def get_profiles(user: User = Depends(decrypt_jwt)):  # noqa
    profiles = await profile_crud.get_profiles()
    return {"profiles": profiles}


@router.get("/{username}/", response_model=ProfileDetail)
async def get_profile(username: str, user: User = Depends(decrypt_jwt)):
    user = await User.get_with_following(user_id=user.id)
    articles_count = len(user.articles)
    following = ...  # noqa
    return {
        "username": user.username,
        "bio": user.bio,
        "image_url": user.image_url,
        "articles_count": articles_count,
        "articles": user.articles,
        "following": ...,
        "followers_count": user.followers_count(),
        "followed_count": user.followed_count(),
    }


@router.post("/{username}/follow/", status_code=status.HTTP_204_NO_CONTENT)
async def follow(username: str, request_user: User = Depends(decrypt_jwt)):
    user = profile_crud.follow_user(username, request_user)
    return user


@router.post("/{username}/unfollow/", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow(username: str, request_user: User = Depends(decrypt_jwt)):
    user = profile_crud.unfollow_user(username, request_user)
    return user
