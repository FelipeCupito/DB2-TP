from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    class Config:
        case_sensitive = True
        env_file = "../.env"


settings = Settings()
