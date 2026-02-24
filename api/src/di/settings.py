from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RIOT_API_KEY: str
    MONGODB_URL: str
    MONGODB_PORT: str
    REDIS_URL: str
    REDIS_PORT: int
    POSTGRES_DB_URL: str
    JAVA_HOME: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
