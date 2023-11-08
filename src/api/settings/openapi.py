from typing import Any, Dict, List

from fastapi.openapi.models import Server, ServerVariable

from api import __version__
from api.settings.base import APIEnv, APISettings, api_config

OPENAPI_API_NAME = "People"
OPENAPI_API_VERSION = __version__
OPENAPI_API_DESCRIPTION = "You know, for people"

DEV_SERVER = dict(
    Server(
        url="http://localhost:8000",
        description="local server",
        variables={},
    )
)
LIVE_SERVERS = dict(
    Server(
        url="https://{server}/api/people/v1",
        description="live server",
        variables={
            "server": ServerVariable(
                enum=["staging.solublecode.dev", "solublecode.dev"],
                default="staging.solublecode.dev",
            )
        },
    )
)
GITHUB_SERVER = dict(
    Server(
        url="https://{subdomain}.githubpreview.dev",
        description="github codespaces",
        variables={"subdomain": ServerVariable(default="")},
    )
)

SERVERS = {
    APIEnv.DEV: [DEV_SERVER],
    APIEnv.PROD: [LIVE_SERVERS, GITHUB_SERVER],
}


class OpenAPISettings(APISettings):
    name: str
    version: str
    description: str
    servers: List[Dict[str, str | Any]]

    @classmethod
    def generate(cls):
        return OpenAPISettings(
            name=f"{api_config.api_env.value} {OPENAPI_API_NAME}",
            version=OPENAPI_API_VERSION,
            description=OPENAPI_API_DESCRIPTION,
            servers=SERVERS[api_config.api_env],
        )


openapi_config = OpenAPISettings.generate()
