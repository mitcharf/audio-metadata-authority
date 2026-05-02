import os

class Settings:
    # Add further config as required
    PROJECT_NAME: str = "Metadata Authority & Library Normalization System"
    VERSION: str = "0.1.0"
    SQLITE_DB_PATH: str = os.getenv("METAAUTH_DB_PATH", "db/metaauth.db")
    DEBUG: bool = os.getenv("DEBUG", "0") == "1"

settings = Settings()
