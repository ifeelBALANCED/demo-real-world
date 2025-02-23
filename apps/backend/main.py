from fastapi import Depends, FastAPI

from api.auth import decrypt_jwt
from api.crud import user as user_crud
from api.schemas.user import RegisterUser

app = FastAPI()


@app.get("/something/")
async def something(token: str = Depends(decrypt_jwt)):
    return {"token": token}


@app.post("/register/")
async def register(user_data: RegisterUser):
    user = await user_crud.create_user(user_data)
    return {"email": user.email, "password": user.hashed_password}


@app.post("/login/")
async def login(user_data: RegisterUser):
    token = await user_crud.verify_user_and_create_jwt(user_data)
    return {"token": token, "token_type": "bearer"}
