import uuid

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from api.models.base import BaseModel


class Article(BaseModel):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True, nullable=False)

    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    body = Column(String, nullable=False)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="articles")

    def __repr__(self):
        return f"<Article {self.title} by {self.author.username}>"
