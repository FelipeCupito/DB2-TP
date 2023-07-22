from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_PORT: int
    MONGO_DB_HOSTNAME: str
    MONGO_DB_DBNAME: str
    MONGO_USERNAME: str
    MONGO_PASSWORD: str

    class Config:
        case_sensitive = True
        env_file = "backend/.env"


settings = Settings()
