import cloudinary.uploader
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Demo App of RealWorld"
    app_version: str = "0.1.0"
    admin_email: str = "admin@example.com"
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "db_name"
    database_user: str = "some_name"
    database_password: str = "some_password"

    # TODO: Make key and iv generate automatically on each server start
    aes_key: str = "invalid_aes_key"
    aes_iv: str = "invalid_aes_iv"
    jwt_secret: str = "invalid_jwt_secret"
    token_expire_minutes: int = 60 * 24

    cloudinary_cloud_name: str = "invalid_cloud_name"
    cloudinary_api_key: str = "invalid_api_key"
    cloudinary_api_secret: str = "invalid_api_secret"

    @property
    def db_creds(self) -> str:
        return f"{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"  # noqa

    @property
    def async_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_creds}"

    @property
    def sync_db_url(self) -> str:
        return f"postgresql://{self.db_creds}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
)
print(settings.dict())
