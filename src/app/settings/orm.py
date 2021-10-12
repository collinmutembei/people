from decouple import config
from pydantic import BaseSettings
from tortoise import Tortoise

from app.settings.base import AppEnv, app_config

DB_MODELS = ["app.models.users", "app.models.socials", "aerich.models"]


class ORMSettings(BaseSettings):
    """Tortoise-ORM settings"""

    db_url: str
    modules: dict
    generate_schemas: bool
    add_exception_handlers: bool

    @classmethod
    def generate(cls):
        if app_config.app_env == AppEnv.LIVE:
            db_url = config("DATABASE_URL")
        elif app_config.app_env == AppEnv.DEV:
            db_url = config("DATABASE_URL", default="sqlite:///tmp/people.db")

        modules = {"models": DB_MODELS}
        return ORMSettings(
            db_url=db_url,
            modules=modules,
            generate_schemas=True if app_config.app_env == AppEnv.DEV else False,
            add_exception_handlers=True if app_config.app_env == AppEnv.DEV else False,
        )


orm_config = ORMSettings.generate()

TORTOISE_ORM = {
    "connections": {
        "default": orm_config.db_url,
    },
    "apps": {
        "models": {**orm_config.modules, "default_connection": "default"},
    },
}

Tortoise.init_models(TORTOISE_ORM["apps"]["models"]["models"], "models")
