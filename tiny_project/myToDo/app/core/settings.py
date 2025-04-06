from pydantic_settings import BaseSettings, ConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Todo API (In-Memory)"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Future PostgreSQL flag
    USE_DATABASE: bool = False
    
    model_config = ConfigDict(env_file=".env")

settings = Settings()