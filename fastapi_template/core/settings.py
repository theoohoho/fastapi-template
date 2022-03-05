from typing import List

from pydantic import AnyHttpUrl, BaseSettings


class JWTSettings(BaseSettings):
    secret_key = "f0fb3cee57236e3d60b4197e6ffc4baa813c17ab706ad9628429f238049c57e4"
    algorithm = "HS256"
    access_token_expire_minutes = 30
    refresh_token_expire_minutes = 60 * 24 * 7

    class Config:
        env_prefix = "JET_"
        env_file = ".env"
        env_file_encoding = "utf-8"


class DatabaseSettings(BaseSettings):
    host: str = "127.0.0.1"
    port: str = "5432"
    username: str = "local_dev"
    password: str = "local_dev"
    name: str = "local_dev"

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

    jwt: JWTSettings = JWTSettings()


settings = Settings()


def get_settings():
    global settings
    if settings:
        return settings
    else:
        return Settings()
