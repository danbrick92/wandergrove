from datetime import datetime, UTC
from logging import Logger
from pydantic.dataclasses import dataclass
from utils.config import Config
from logs.json_logger import get_json_logger


@dataclass(config=dict(arbitrary_types_allowed=True))
class Context:
    config: Config
    logger: Logger
    dt: datetime

    @classmethod
    def bootstrap(cls) -> "Context":
        config = Config()
        dt = cls._get_datetime()
        return Context(config=config, logger=get_json_logger(config.logging_level), dt=dt)

    @classmethod
    def _get_datetime(cls) -> datetime:
        return datetime.now(tz=UTC)

    @property
    def dt_str(self) -> str:
        return self.dt.strftime(self.config.datetime_fmt)
