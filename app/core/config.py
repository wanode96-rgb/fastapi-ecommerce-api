from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()

# What happens internally
# When app starts:
# 1. Settings() is created
# 2. It reads .env
# 3. Validates types
# 4. Stores values in settings