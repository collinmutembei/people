from enum import Enum

from decouple import config
from pydantic_settings import BaseSettings


class APIEnv(str, Enum):
    """
    Change API settings dynamically based on environment
    """

    DEV = "🛠"
    PROD = "🌍"


class APISettings(BaseSettings):
    api_env: APIEnv = config("API_ENV", default=APIEnv.DEV)
    db_url: str = config("DATABASE_URL", default="mongodb://localhost:27017")
    # TODO: #87 Add Email settings

    @classmethod
    def generate(cls):
        return APISettings()


api_config = APISettings.generate()
