from pydantic import BaseSettings
from pathlib import Path

BASE_DIR = Path.cwd()


class Settings(BaseSettings):
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_BASE: str = "fastapi"
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    TOKEN: str = "1234567890:FKSJNDNDJ445ferfsdSFFfergfeg"

    @property
    def DB_URL(self) -> str:
        """
        Assemble Database URL from settings.
        :return: Database URL.
        """

        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_BASE}"

    class Config:
        env_file = f"{BASE_DIR}/.env"
        fields = {
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
            },
            "TOKEN": {
                "env": "TELEGRAM_TOKEN"
            }
        }

settings = Settings()
