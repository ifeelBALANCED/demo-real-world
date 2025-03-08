import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import joinedload, relationship

from api.models.base import BaseModel
from engine import Base, get_db

follow_association_table = Table(
    "user_follows",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("followed_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    bio = Column(String)
    image_url = Column(String)
    following = relationship(
        "User",
        secondary=follow_association_table,
        primaryjoin=id == follow_association_table.c.follower_id,
        secondaryjoin=id == follow_association_table.c.followed_id,
    )
    followers = relationship(
        "User",
        secondary=follow_association_table,
        primaryjoin=id == follow_association_table.c.followed_id,
        secondaryjoin=id == follow_association_table.c.follower_id,
    )
    articles = relationship("Article", back_populates="author", cascade="all, delete-orphan")

    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    @classmethod
    async def get_with_following(cls, user_id: int) -> "User":
        async for session in get_db():
            result = await session.execute(select(cls).options(joinedload(cls.following)).filter_by(id=user_id))
            return result.scalars().first()

    def followers_count(self) -> int:
        return len(self.followers)

    def followed_count(self) -> int:
        return len(self.following)
