from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    open_weather_map_api_key: str
    db_url: str

    class Config:
        env_file = ".env"


settings = Settings()
