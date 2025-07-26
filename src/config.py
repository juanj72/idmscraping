import os
from typing import Any, Dict

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.config: Dict[str, Any] = {
            "env": self._get_env_var("ENV", str, default="development"),
            "database": {
                "host": self._get_env_var("DATABASE_HOST", str, default="localhost"),
                "port": self._get_env_var("DATABASE_PORT", str, default=3306),
                "name": self._get_env_var("DATABASE_NAME", str, default="idmscraping"),
                "user": self._get_env_var("DATABASE_USER", str, default="root"),
                "password": self._get_env_var("DATABASE_PASSWORD", str, default=""),
            },
        }

    def _get_env_var(self, name, expected_type, default=None):
        value = os.getenv(name)

        if value is None:
            if default is not None:
                return default
            raise ValueError(f"Environment variable {name} not set")

        if not isinstance(value, expected_type):
            raise TypeError(
                f"Environment variable {name} is not of type {expected_type.__name__}"
            )

        return value
