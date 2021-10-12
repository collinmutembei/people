from app.settings.base import AppSettings, app_config

OPENAPI_API_NAME = "People"
OPENAPI_API_VERSION = "0.0.1"
OPENAPI_API_DESCRIPTION = "You know, for people"


class OpenAPISettings(AppSettings):
    name: str
    version: str
    description: str

    @classmethod
    def generate(cls):
        return OpenAPISettings(
            name=f"{OPENAPI_API_NAME}:{app_config.app_env}",
            version=OPENAPI_API_VERSION,
            description=OPENAPI_API_DESCRIPTION,
        )


openapi_config = OpenAPISettings.generate()
