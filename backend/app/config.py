from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    SQLALCHEMY_DATABASE_URL: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
