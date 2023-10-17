from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


class Settings(BaseSettings):
    APP_HOST: str = "localhost"
    APP_PORT: int = os.getenv("APP_PORT")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")


load_dotenv()
env = Settings()
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{env.DB_USER}:{env.DB_PASSWORD}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}?autocommit=true&charset=utf8mb4"
