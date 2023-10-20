from typing import Any, Dict, List

from fastapi.openapi.models import Server, ServerVariable

from app.settings.base import AppEnv, AppSettings, app_config

OPENAPI_API_NAME = "People"
OPENAPI_API_VERSION = "1.0.0"
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
    AppEnv.DEV: [DEV_SERVER],
    AppEnv.PROD: [LIVE_SERVERS, GITHUB_SERVER],
}


class OpenAPISettings(AppSettings):
    name: str
    version: str
    description: str
    servers: List[Dict[str, str | Any]]

    @classmethod
    def generate(cls):
        return OpenAPISettings(
            name=f"{app_config.app_env.value} {OPENAPI_API_NAME}",
            version=OPENAPI_API_VERSION,
            description=OPENAPI_API_DESCRIPTION,
            servers=SERVERS[app_config.app_env],
        )


openapi_config = OpenAPISettings.generate()
