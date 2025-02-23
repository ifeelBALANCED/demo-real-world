from pydantic_settings import BaseSettings

from utils import EnvParser

env = EnvParser()


class Settings(BaseSettings):
    app_name: str = "Demo App of RealWorld"
    admin_email: str = env.str("ADMIN_EMAIL", "admin@example.com")
    database_host: str = env.str("DATABASE_HOST", "localhost")
    database_port: int = env.int("DATABASE_PORT", 5432)
    database_name: str = env.str("DATABASE_NAME", "db_name")
    database_user: str = env.str("DATABASE_USER", "some_name")
    database_password: str = env.str("DATABASE_PASSWORD", "some_password")

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
print(settings.sync_db_url)
