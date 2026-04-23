import logging
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from hnp.hnp_config import HNPConfig


# class DatabaseConfig(BaseSettings):
#     # Pydantic will check if this is a valid URL, not just a string
#     url: PostgresDsn = "postgresql://user:pass@localhost:5432/db"
#     pool_size: int = 20


class Config(BaseSettings):
    datetime_fmt: str = "Y%m%dT%H%M%S"
    logging_level: int = logging.INFO
    hnp: HNPConfig = HNPConfig()

    # model_config = SettingsConfigDict(
    #     env_prefix="MYAPP_", # Looks for MYAPP_DEBUG in shell
    #     env_file=".env",
    #     extra="ignore"       # Don't crash if extra env vars exist
    # )
    # debug: bool = False
    # api_key: str = Field(..., alias="SECRET_KEY") # Map different names
    # db: DatabaseConfig = DatabaseConfig()
