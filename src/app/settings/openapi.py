from typing import Any, Dict, List, Union

from fastapi.openapi.models import Server, ServerVariable

from app.settings.base import AppSettings, app_config

OPENAPI_API_NAME = "people"
OPENAPI_API_VERSION = "0.0.1"
OPENAPI_API_DESCRIPTION = "You know, for people"

DEV_SERVER = Server(
    url="http://localhost:8000",
    description="local server",
    variables={},
)
LIVE_SERVER = Server(
    url="https://{server}/v1/people",
    description="online server",
    variables={
        "server": ServerVariable(
            enum=["staging.solublecode.api", "solublecode.api"],
            default="staging.solublecode.api",
        )
    },
)


class OpenAPISettings(AppSettings):
    name: str
    version: str
    description: str
    servers: List[Dict[str, Union[str, Any]]]

    @classmethod
    def generate(cls):
        return OpenAPISettings(
            name=f"{app_config.app_env} {OPENAPI_API_NAME}",
            version=OPENAPI_API_VERSION,
            description=OPENAPI_API_DESCRIPTION,
            servers=[DEV_SERVER, LIVE_SERVER],
        )


openapi_config = OpenAPISettings.generate()
