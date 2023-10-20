from enum import Enum

from decouple import config
from pydantic_settings import BaseSettings


class AppEnv(str, Enum):
    """
    Change app settings dynamically based on environment
    """

    DEV = "🛠"
    PROD = "🌍"


class AppSettings(BaseSettings):
    app_env: AppEnv = config("APP_ENV", default=AppEnv.DEV)
    db_url: str = config("DATABASE_URL", default="mongodb://localhost:27017")

    @classmethod
    def generate(cls):
        return AppSettings()


app_config = AppSettings.generate()
