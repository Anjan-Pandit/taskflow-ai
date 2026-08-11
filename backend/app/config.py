from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME","TaskFlow AI")

    APP_VERSION = os.getenv("APP_VERSION","1.0.0")

    DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///./taskflow.db")
settings = Settings()