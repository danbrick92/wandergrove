from pydantic_settings import BaseSettings
from utils.raw_object import RawObject


class SinasConfig(BaseSettings):
    source_name: str = "sinas"
    raw_objects: list[RawObject] = [
        RawObject(
            url="https://zenodo.org/records/18220953/files/SInAS_3.1.1.csv?download=1",
            filename="SInAS_3.1.1.csv",
            timeout=20.0,
            mode="wb"
        )
    ]
