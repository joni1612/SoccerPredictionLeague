from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SoccerPredictionLeague"
    DEBUG: bool = False
    DATABASE_URL: str

    model_config = {"env_file": ".env"}


settings = Settings()
