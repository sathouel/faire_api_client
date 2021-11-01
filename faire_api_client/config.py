from pydantic import BaseSettings

class Settings(BaseSettings):
    API_VERSION: str = 'v2'
    BASE_URL: str = 'https://www.faire.com/external-api'

settings = Settings()