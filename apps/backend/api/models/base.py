import re
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import (
    DuplicateRecordError,
    MissingFieldsError,
    MultipleRecordsFound,
    RecordNotFound,
)
from engine import Base, get_db


class BaseModel(Base):
    __abstract__ = True  # This makes BaseModel an abstract class, not a table

    @classmethod
    async def _get_db_session(cls) -> AsyncSession:
        async for session in get_db():
            return session
        raise Exception("Could not retrieve database session")

    @classmethod
    async def filter(cls, **fields) -> Sequence:
        db_session = await cls._get_db_session()
        query = select(cls)
        for field_name, value in fields.items():
            if hasattr(cls, field_name):
                column = getattr(cls, field_name)
                query = query.filter(column == value)

        result = await db_session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get(cls, **fields) -> "BaseModel":
        results = await cls.filter(**fields)

        if not results:
            raise RecordNotFound(cls.__name__)
        if len(results) > 1:
            raise MultipleRecordsFound(cls.__name__)
        return results[0]

    @classmethod
    async def create(cls, **fields) -> "BaseModel":
        db_session = await cls._get_db_session()
        try:
            instance = cls(**fields)
            db_session.add(instance)
            await db_session.commit()
            await db_session.refresh(instance)
        except IntegrityError as e:
            error_message = str(e.orig).lower()
            duplicate_field = None
            missing_field = None

            # Identify the duplicate field in unique constraint violation error message
            duplicate_match = re.search(r"key \((.+?)\)=", error_message)
            if duplicate_match:
                duplicate_field = duplicate_match.group(1)

            # Identify the missing field from error message
            missing_match = re.search(r'null value in column "([^"]+)"', error_message)
            if missing_match:
                missing_field = missing_match.group(1)

            if "duplicate" in error_message or "unique constraint" in error_message:
                raise DuplicateRecordError(cls.__name__, field=duplicate_field)
            if "null value in column" in error_message or "not-null" in error_message:
                raise MissingFieldsError(cls.__name__, field=missing_field)
            raise e
        return instance

    async def update(self, **fields) -> "BaseModel":
        db_session = await self.__class__._get_db_session()
        try:
            for key, value in fields.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            await db_session.commit()
            await db_session.refresh(self)
        except IntegrityError as e:
            await db_session.rollback()
            error_message = str(e.orig).lower()
            duplicate_field = None
            missing_field = None

            duplicate_match = re.search(r"key \((.+?)\)=", error_message)
            if duplicate_match:
                duplicate_field = duplicate_match.group(1)

            missing_match = re.search(r'null value in column "([^"]+)"', error_message)
            if missing_match:
                missing_field = missing_match.group(1)

            if "duplicate" in error_message or "unique constraint" in error_message:
                raise DuplicateRecordError(self.__class__.__name__, field=duplicate_field)
            if "null value in column" in error_message or "not-null" in error_message:
                raise MissingFieldsError(self.__class__.__name__, field=missing_field)
            raise e
        return self
