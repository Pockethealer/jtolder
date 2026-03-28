from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Pydantic will automatically look for these keys in the .env file
    DATABASE_URL: str
    SECRET_KEY: str

    # This tells Pydantic where to find the .env file (one folder up from /backend)
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

# Create a global instance to use throughout your app
settings = Settings()