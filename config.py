from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PORT: int = 8080
    ENVIRONMENT: str= "dev"
    UI_HOST: str = "localhost:3000"
    
    DATABASE_URL: str = "sqlite:///pocTemp.db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600

settings = Settings()
