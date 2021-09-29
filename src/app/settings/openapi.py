from app.settings.base import AppSettings

OPENAPI_API_NAME = "API"
OPENAPI_API_VERSION = "0.0.1"
OPENAPI_API_DESCRIPTION = "You know, for API"


class OpenAPISettings(AppSettings):
    name: str
    version: str
    description: str

    @classmethod
    def generate(cls):
        return OpenAPISettings(
            name=OPENAPI_API_NAME,
            version=OPENAPI_API_VERSION,
            description=OPENAPI_API_DESCRIPTION,
        )


openapi_config = OpenAPISettings.generate()
