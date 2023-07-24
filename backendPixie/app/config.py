from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str

    PORT: int
    HOST: str

    DATABASE_PORT: str
    MONGO_DB_HOSTNAME: str
    MONGO_DB_DBNAME: str
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_DB_HOST: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
