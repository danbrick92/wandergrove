"""
This script handles scraping Doug Tallamy's Homegrown National Park.
It does not currently scrape plant data, only the keystone plants to a particular ecoregion.
It creates a csv file for now - later it can go to Postgres.
"""
from typing import List, TypeAlias, Tuple
from itertools import islice
import logging
import json
import asyncio
import polars as pl
from pydantic import BaseModel
import httpx
from bs4 import BeautifulSoup
from utils.base_pipeline_handler import BasePipelineHandler
from utils.context import Context
from hnp.hnp_keystone_plant import HNPKeystonePlant
from hnp.hnp_keystone_plant_ecoregion import HNPKeystonePlantEcoregion
from hnp.hnp_exceptions import ScrapingException, MissingPlantsException


T_out: TypeAlias = Tuple[List[HNPKeystonePlant], List[HNPKeystonePlantEcoregion]]

# Silence httpx
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


class Ecoregion(BaseModel):
    slug: str
    name: str
    count: int


class HomegrownNationalParkHandler(BasePipelineHandler[None, T_out]):
    async def run_pipeline(self) -> T_out:
        """
        We are going to scrape https://homegrownnationalpark.org/keystone-plants
        The url has the ecoregion appended (ie: ?_ecoregion=2-2-alaska-tundra-usa)
        Step 1 - Get all the ecoregions 
        Step 2 - Scrape each ecoregion for available plants, adding new pages to the queue as needed
        Step 3 - Scrape each plant
        """
        ecoregions = self.__get_all_ecoregions()
        batch_size = self.context.config.hnp.batch_size
        plant_ecoregions: List[HNPKeystonePlantEcoregion] = []
        self.log("Scraping for all plants")
        for i in range(0, len(ecoregions), batch_size):
            self.log(f"Processing ecoregions: {i}:{i + batch_size}")
            current_batch_regions = ecoregions[i : i + batch_size]
            tasks = [
                self.__scrape_ecoregion_page(
                    ecoregion=region,
                    plants=[],
                    count=region.count,
                    page=1
                ) 
                for region in current_batch_regions
            ]
            results = await asyncio.gather(*tasks)
            for r in results:
                plant_ecoregions.extend(r)

        self.log(f"Found {len(plant_ecoregions)} plants")
        self.__convert_to_csv(plant_ecoregions)

    def __construct_url(self, slug: str, page: int = 1) -> str:
        return f"{self.context.config.hnp.base_url}/page/{page}/?_ecoregion={slug}"        

    def __get_all_ecoregions(self) -> List[Ecoregion]:
        # Get the webpage
        self.log("Getting all ecoregions for HNP")
        url = self.__construct_url(self.context.config.hnp.starting_slug)
        response = httpx.get(url, follow_redirects=True)

        # Navigate to ecoregions data
        soup = BeautifulSoup(response.content, 'html.parser')
        script_tag = soup.find('script', id='search-filter-data-js')
        if not script_tag:
            raise ScrapingException("Could not find ecoregions")
        raw_data = script_tag.get('data-search-filter-data')
        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError as e:
            raise ScrapingException("Unable to load ecoregions json") from e
        fields = data.get('fields')
        if not fields:
            raise ScrapingException("Unable to parse ecoregions json") from e

        # Find the ecoregions
        ecoregions: List[Ecoregion] = []
        for field_id, field_data in fields.items():
            if field_data.get('attributes', {}).get('dataTaxonomy') != 'ecoregion':
                continue
            options = field_data.get('options', [])
            for opt in options:
                ecoregion = Ecoregion(
                    name=opt.get("label"),
                    slug=opt.get("value"),
                    count=opt.get("count")
                )
                ecoregions.append(ecoregion)
        self.log(f"Found {len(ecoregions)} ecoregions")
        return ecoregions

    async def __scrape_ecoregion_page(
        self,
        ecoregion: Ecoregion,
        plants: List[HNPKeystonePlantEcoregion],
        count: int,
        page: int = 1
    ) -> List[HNPKeystonePlantEcoregion]:
        url = self.__construct_url(ecoregion.slug, page)
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)

        soup = BeautifulSoup(response.content, 'html.parser')
        plant_entries = soup.find_all(class_="plant-list-entry")
        count -= len(plant_entries)

        for entry in plant_entries:
            title_link = entry.find('h3').find('a')
            common_name = title_link.get_text(strip=True)
            link = title_link.get('href')
            latin_name = entry.find('div', class_='plant-list-entry-left').find('p').get_text(strip=True)
            plant = HNPKeystonePlantEcoregion(
                common_name=common_name,
                latin_name=latin_name,
                ecoregion=ecoregion.name,
                ecoregion_url=url,
                plant_url=link
            )
            plants.append(plant)

        if count > 0:
            plants = await self.__scrape_ecoregion_page(ecoregion, plants, count, page+1)
        if len(plants) != ecoregion.count:
            raise MissingPlantsException(f"Missing plants. Found: {ecoregion.count}. Expected: {len(plants)}")
        return plants

    def __convert_to_csv(self, plant_ecoregions: List[HNPKeystonePlantEcoregion]) -> None:
        df = pl.from_dicts([p.model_dump() for p in plant_ecoregions])
        df_unique = df.unique(subset=["latin_name", "ecoregion"], maintain_order=True)
        removed_count = len(df) - len(df_unique)
        if removed_count > 0:
            self.log(f"Removed {removed_count} duplicate plant-ecoregion entries.")
        plant_ecoregions_filename = self.context.config.hnp.plant_ecoregions_filename
        path = self.context.config.hnp.base_export_path.joinpath(plant_ecoregions_filename)
        df_unique.write_csv(path)
        self.log(f"Wrote results to: {path}")


def main():
    context = Context.bootstrap()
    handler = HomegrownNationalParkHandler(context)
    asyncio.run(handler.run_pipeline())


if __name__ == "__main__":
    main()
