from typing import List
from pydantic import BaseSettings, AnyHttpUrl


class DatabaseSettings(BaseSettings):

    host: str = ""
    port: str = ""
    username: str = ""
    password: str = ""
    name: str = ""

    class Config:
        env_prefix = "DB_"
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def db_url(self):
        return "postgresql://{user}:{pwd}@{host}:{port}/{db}".format(
            user=self.username,
            pwd=self.password,
            host=self.host,
            port=self.port,
            db=self.name,
        )


class Settings(BaseSettings):
    app_name = "FastAPI_Template"
    version = "0.1.0"
    env: str = "dev"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    cors_origin: List[AnyHttpUrl] = []

    database: DatabaseSettings = DatabaseSettings()


settings = Settings()
