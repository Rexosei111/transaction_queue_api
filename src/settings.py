from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str
    jwt_expire_time: int
    jwt_forgot_otp_secret: str
    jwt_forgot_otp_expire_time: int
    algorithm: str
    postgres_database_url: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
