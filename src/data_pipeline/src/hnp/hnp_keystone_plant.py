from pydantic import BaseModel, Field, ConfigDict


class HNPKeystonePlant(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    latin_name: str = Field(alias="LatinName")
    common_name: str = Field(alias="CommonName")
    plant_url: str = Field(alias="PlantUrl")
    plant_types: str = Field(alias="PlantTypes")
    watering_needs: str = Field(alias="WateringNeeds")
    light_requirements: str = Field(alias="LightRequirements")
    season_of_interest: str = Field(alias="SeasonOfInterest")
    height: str = Field(alias="Height")
    spread: str = Field(alias="Spread")
    duration: str = Field(alias="Duration")
