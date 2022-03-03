from typing import List
from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    app_name = "FastAPI_Template"
    version = "0.1.0"
    env: str = "dev"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    cors_origin: List[AnyHttpUrl] = []


settings = Settings()
