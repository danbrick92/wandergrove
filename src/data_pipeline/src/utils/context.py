from typing import Self
from logging import Logger
from pydantic.dataclasses import dataclass
from utils.config import Config
from logs.json_logger import get_json_logger


@dataclass(config=dict(arbitrary_types_allowed=True))
class Context:
    config: Config
    logger: Logger

    @classmethod
    def bootstrap(cls) -> Self:
        config = Config()
        return Context(
            config=config,
            logger=get_json_logger(config.logging_level)
        )
