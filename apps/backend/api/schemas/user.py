from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator


class RegisterUser(BaseModel):
    email: str
    password: str
    username: str

    # TODO: Add validation for username
    # TODO: Improve email validation

    @field_validator("email")
    def validate_email(cls, email: str) -> str:
        if not email:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email is required")
        return email

    @field_validator("password")
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


class LoginUser(BaseModel):
    email: str
    password: str

    # TODO: Make common validators for email and password


class UpdateUser(BaseModel):
    password: str
    username: str
