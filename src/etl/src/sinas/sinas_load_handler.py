from pathlib import Path
from utils.base_load_handler import BaseLoadHandler
from utils.raw_object import RawObject
from sinas.sinas_model import SinasModel
import polars as pl


"""
## TODO
Download & Load Handler - only support one handler per file - simplifies transform and load functions
Load into Postgres (use metadata table to determine if there were updates)
"""

class SinasLoadHandler(BaseLoadHandler):
    async def _load_df(self, path: Path) -> None:
        df = await self.load_dataframe(path)
        SinasModel.validate(df)
        SinasModel.post_validate(df)

    async def load_dataframe(self, path: Path) -> pl.DataFrame:
        return pl.read_csv(path, separator=" ")

    def _get_source_name(self) -> str:
        return self.config.sinas.source_name

    def _get_raw_objects(self) -> list[RawObject]:
        return self.config.sinas.raw_objects
