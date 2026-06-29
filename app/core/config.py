from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SoccerPredictionLeague"
    DEBUG: bool = False
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7

    model_config = {"env_file": ".env"}


settings = Settings()
