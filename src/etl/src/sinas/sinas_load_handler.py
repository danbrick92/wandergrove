from utils.base_handler import BaseHandler
from sinas.sinas_model import SinasModel
import polars as pl


class SinasLoadHandler(BaseHandler):
    async def run_handler(self) -> None:
        path = "/Users/danielbrickner/data/raw/sinas/20260807T192653/SInAS_3.1.1.csv"
        df = pl.read_csv(path, separator=" ")
        SinasModel.validate(df)
        SinasModel.post_validate(df)
