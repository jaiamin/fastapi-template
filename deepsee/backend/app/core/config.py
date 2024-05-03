import os

from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='./.env', env_file_encoding='utf-8', case_sensitive=True
    )

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    SERVER_HOST: str
    SERVER_PORT: int

    PROJECT_NAME: str

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme='postgresql',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
    


class ContainerDevSettings(Settings):
    model_config = SettingsConfigDict(
        env_file='./.env', env_file_encoding='utf-8', case_sensitive=True
    )
    ENV: str = 'dev'


def get_settings(env: str = 'dev') -> Settings:
    """
    Return the settings object based on the environment.
    """

    if env.lower() in ['dev', 'd', 'development']:
        return ContainerDevSettings()
    
    raise ValueError('Invalid environment. Must be "dev"')


_env = os.environ.get('ENV', 'dev')

settings = get_settings(env=_env)