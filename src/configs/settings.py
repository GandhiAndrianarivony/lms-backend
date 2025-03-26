from pydantic_settings import BaseSettings, SettingsConfigDict

# Load from environment variables
class JWTConfigs(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION: int


# Load from .env file
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
