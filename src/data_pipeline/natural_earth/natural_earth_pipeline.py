from data_pipeline.a_data_pipeline import ADataPipeline
from data_pipeline.natural_earth.natural_earth_config import NaturalEarthConfig
from data_pipeline.natural_earth.natural_earth_scraper import NaturalEarthWebScraper
from enum import Enum
from pathlib import Path
from typing import Union, List


class NaturalEarthPipeline(ADataPipeline):
    def __init__(self, config: NaturalEarthConfig) -> None:
        self.config = config
        
    def load_urls(self, urls_path: Path) -> List[str]:
        """
        Given a text file path and a text file of urls separated by line,
        return them as a list of urls
        """
        if not urls_path.is_file():
            raise FileNotFoundError(f"Unable to locate: {urls_path}")
        with open(urls_path, 'r') as file:
            urls = file.read().splitlines()
        urls = [url.strip() for url in urls if url.strip() != ""]
        return urls
        
    def extract(
        self,
        data_path: Path,
        urls: Union[List[str], None] = None,
        scraper_override: Union[NaturalEarthWebScraper, None] = None
    ) -> List[Path]:
        print("Running Natural Earth extraction pipeline")
        # Setup scraper
        if scraper_override is not None:
            scraper = scraper_override
        else:
            scraper = NaturalEarthWebScraper(
                base_url = self.config.scraper_base_url,
                suffix = self.config.scraper_suffix,
                contains_filters=self.config.contains_filters
            )
            
        # Scrape if urls not provided
        if urls is None:
            urls = scraper.scrape()
            
        # Generate paths from base path
        downloaded_files: List[str] = []
        for url in urls:
            path_parts = url.split("/download/")[1].split("/")
            path = data_path.joinpath(*path_parts)
            scraper.download_file(url, True, path)
            downloaded_files.append(path)
            
        return downloaded_files
