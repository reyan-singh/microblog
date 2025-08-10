import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "mysql+asyncmy://user:password@localhost/microblog")
    REDIS_URL: str = os.environ.get("REDIS_URL", "redis://localhost")
    SECRET_KEY: str = "a_very_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()