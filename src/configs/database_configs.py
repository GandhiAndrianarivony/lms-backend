from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgreSQLConfigs(BaseSettings):
    USER: str
    PASSWORD: str
    DB: str
    HOST: str
    PORT: int

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
        env_file=".env",
        extra="ignore",
    )


pg_configs = PostgreSQLConfigs()
