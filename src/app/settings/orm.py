from decouple import config
from tortoise import Tortoise

from app.settings.base import AppSettings

DB_MODELS = ["app.models.users", "app.models.socials", "aerich.models"]

DEBUG = config("DEBUG", default=False, cast=bool)


class ORMSettings(AppSettings):
    """Tortoise-ORM settings"""

    db_url: str
    modules: dict
    generate_schemas: bool
    add_exception_handlers: bool

    @classmethod
    def generate(cls):
        db_url = config("DATABASE_URL", default="sqlite://:memory:")
        modules = {"models": DB_MODELS}
        return ORMSettings(
            db_url=db_url,
            modules=modules,
            generate_schemas=True if DEBUG else False,
            add_exception_handlers=True if DEBUG else False,
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
