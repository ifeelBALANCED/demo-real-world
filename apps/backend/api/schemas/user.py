from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator


class CommonUserFieldsValidatorMixin:
    """Mixin class for reusable Pydantic field validators."""

    # TODO: Add validation for username
    # TODO: Improve email validation

    @field_validator("email", check_fields=False)
    def validate_email(cls, email: str) -> str:
        if not email:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email is required")
        return email

    @field_validator("password", check_fields=False)
    def validate_password(cls, password: str) -> str:
        if not password:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password is required")
        if len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters long"
            )
        if not any(char.isdigit() for char in password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain at least one digit"
            )
        if not any(char.isalpha() for char in password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain at least one letter"
            )
        return password

    @field_validator("username", check_fields=False)
    def validate_username(cls, username: str) -> str:
        return username


class RegisterUser(BaseModel, CommonUserFieldsValidatorMixin):
    email: str
    password: str
    username: str


class LoginUser(BaseModel, CommonUserFieldsValidatorMixin):
    email: str
    password: str

    # TODO: Make common validators for email and password


class LoginResponse(BaseModel):
    token: str
    token_type: str


class UpdateUser(BaseModel, CommonUserFieldsValidatorMixin):
    password: str
    username: str


class DetailUser(BaseModel):
    email: str
    username: str
    image_url: Optional[str]
    bio: Optional[str]
