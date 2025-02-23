import base64
from datetime import UTC, datetime, timedelta

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from api.models import User
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
AES_KEY = bytes.fromhex(settings.aes_key)
AES_IV = bytes.fromhex(settings.aes_iv)


def create_jwt(user: User):
    payload = {
        "user_uuid": str(user.uuid),
        "exp": datetime.now(UTC) + timedelta(minutes=settings.token_expire_minutes),
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=default_backend())
    encryptor = cipher.encryptor()

    pad_len = 16 - (len(token) % 16)
    padded_token = token + (" " * pad_len)
    encrypted_token = encryptor.update(padded_token.encode()) + encryptor.finalize()

    return base64.urlsafe_b64encode(encrypted_token).decode()


async def decrypt_jwt(token: str = Depends(oauth2_scheme)) -> User:
    try:
        encrypted_token = base64.urlsafe_b64decode(token)

        cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_token = decryptor.update(encrypted_token) + decryptor.finalize()

        token = decrypted_token.decode().rstrip()
        decoded = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        return await User.get(uuid=decoded["user_uuid"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
