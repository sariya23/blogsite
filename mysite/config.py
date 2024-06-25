from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    db_name: str
    db_username: str
    db_password: str
    db_host: str
    allowed_hosts: list[str]
    model_config = SettingsConfigDict(env_file=".env")


envs = Settings()  # type: ignore