from typing import Optional

from pydantic import BaseModel

from api.schemas.article import ArticleList


class ProfileDetail(BaseModel):
    username: str
    bio: Optional[str] = None
    image_url: Optional[str] = None
    articles_count: int
    articles: ArticleList
    following: bool
    followers_count: int
    followed_count: int


class ProfileList(BaseModel):
    profiles: list[ProfileDetail]
