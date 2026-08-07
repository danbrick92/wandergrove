from pydantic import BaseModel, Field, ConfigDict


class HNPKeystonePlantEcoregion(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    common_name: str = Field(alias="CommonName")
    latin_name: str = Field(alias="LatinName")
    ecoregion: str = Field(alias="Ecoregion")
    ecoregion_url: str = Field(alias="EcoregionUrl")
    plant_url: str = Field(alias="PlantUrl")
