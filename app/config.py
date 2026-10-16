from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:admin@localhost:5432/notification"
    jwt_secret: str = "super-secret-key-for-testing"
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()