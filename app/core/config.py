from pathlib import Path
from sys import modules

from pydantic import BaseSettings

# BASE_DIR = Path(__file__).parent.resolve()
# BASE_DIR = Path.cwd()


class Settings(BaseSettings):
    """Application settings."""

    ENV: str = "dev"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    _BASE_URL: str = f"https://{HOST}:{PORT}"
    # quantity of workers for uvicorn
    WORKERS_COUNT: int = 1
    # Enable uvicorn reloading
    RELOAD: bool = False
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_BASE: str = "db"
    DB_ECHO: bool = False

    @property
    def BASE_URL(self) -> str:
        return self._BASE_URL if self._BASE_URL.endswith("/") else f"{self._BASE_URL}/"

    @property
    def DB_URL(self) -> str:
        """
        Assemble Database URL from settings.
        :return: Database URL.
        """

        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_BASE}"

    class Config:
        # env_file = f"{BASE_DIR}/.env"
        # env_file_encoding = "utf-8"
        fields = {
            "_BASE_URL": {
                "env": "BASE_URL",
            },
            "DB_BASE": {
                "env": "DB_BASE",
            },
            "DB_HOST": {
                "env": "DB_HOST"
                },
            "DB_PORT": {
                "env": "DB_PORT"
            },
            "DB_USER": {
                "env": "DB_USER"
            },
            "DB_PASS": {
                "env": "DB_PASS"
            }
        }


settings = Settings()
