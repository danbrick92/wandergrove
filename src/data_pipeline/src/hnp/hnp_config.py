from pydantic_settings import BaseSettings
from pathlib import Path


class HNPConfig(BaseSettings):
    base_url: str = "https://homegrownnationalpark.org/keystone-plants"
    starting_slug: str = "8-4-ozark-ouachita-appalachian-forests"
    count_per_page: int = 18
    batch_size: int = 10
    
    base_export_path: Path = Path(__file__).parents[2].joinpath("data")
    plant_ecoregions_filename: str = "hnp_keystone_plant_ecoregions.csv"
    
