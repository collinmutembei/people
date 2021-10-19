from enum import Enum

from decouple import config
from pydantic import BaseSettings


class AppEnv(str, Enum):
    """
    Change app settings dynamically based on environment
    """

    DEV = "🛠"
    PROD = "🌍"


class AppSettings(BaseSettings):
    app_env: AppEnv = config("APP_ENV", default=AppEnv.PROD)

    @classmethod
    def generate(cls):
        return AppSettings()


app_config = AppSettings.generate()
