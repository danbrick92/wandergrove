from data_pipeline.a_data_pipeline import ADataPipeline
from data_pipeline.natural_earth.natural_earth_config import NaturalEarthConfig
from data_pipeline.natural_earth.natural_earth_scraper import NaturalEarthWebScraper
from utils.io import unzip_to_directory, list_files_under_path
from enum import Enum
from pathlib import Path
from typing import Union, List, Tuple


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
        zips_path: Union[Path, None] = None,
        scraper_override: Union[NaturalEarthWebScraper, None] = None
    ) -> None:
        """
        Perform the extraction process - scrape, download, extract zips
        
        Args:
            data_path (Path): The path where data should be extracted to
            urls (List[str] | None): To skip scraping, provide a list directly of urls here
            zips_path (Path | None): To skip downloading zips, provide the path where the zip files are
            scraper_override (NaturalEarthWebScraper | None): To override scraper, pass initialized one here
        """
        print("Running Natural Earth extraction pipeline")
        
        # Scrape
        scraper, urls = self.__scrape(scraper_override, urls)
            
        # Download
        downloaded_files = self.__download_urls(urls, data_path, scraper, zips_path)
        
        # Extract
        self.__extract_zips(downloaded_files)
    
    def __scrape(
        self, 
        scraper_override: Union[NaturalEarthConfig, None], 
        urls: List[str]
    ) -> Tuple[NaturalEarthWebScraper, List[str]]:
        # Setup scraper
        if scraper_override is not None:
            scraper = scraper_override
        else:
            scraper = NaturalEarthWebScraper(
                base_url = self.config.scraper_base_url,
                suffix = self.config.scraper_suffix,
                contains_filters=self.config.pipeline_contains_filters
            )
            
        # Scrape if urls not provided
        if urls is None:
            print("Scraping Natural Earth")
            urls = scraper.scrape()
            
        # If all-inclusive zips are included in urls, remove other related ones
        for alz in self.config.pipeline_all_inclusive_zips:
            size_filter = alz.split("_")[0]
            type_filter = alz.split("_")[1].split(".")[0]
            urls = [url for url in urls if not (size_filter in url and type_filter in url and alz not in url)]
            
        return scraper, urls
    
    def __download_urls(
        self, 
        urls: List[str], 
        data_path: Path, 
        scraper: NaturalEarthWebScraper, 
        zips_path: Union[Path, None]
    ) -> List[Path]:
        # Process zips path
        if isinstance(zips_path, Path):
            return list_files_under_path(zips_path)
        
        print(f"Downloading {len(urls)} files.")
        downloaded_files: List[Path] = []
        for url in urls:
            path_parts = url.split("/download/")[1].split("/")
            path = data_path.joinpath(*path_parts)
            scraper.download_file(url, True, path)
            downloaded_files.append(path)
        return downloaded_files
    
    def __extract_zips(self, downloaded_files: List[Path]) -> None:
        # Extract downloaded zip files
        unzipped_files = []
        print("Extracting zip files.")
        for file in downloaded_files:
            # Validate it's a zip file
            if not file.name.endswith(".zip"):
                print(f"Skipping extraction of {file} since it is not a zip file.")
                continue
            
            # Determine extract path
            new_dir = file.name.removesuffix(".zip")
            extract_path = Path.joinpath(file.parent, new_dir)
            if extract_path.is_dir():
                print(f"File {file} will not be extracted since a directory exists already: {extract_path}")
                continue
            
            # Make directory
            extract_path.mkdir(parents=True, exist_ok=True)
            
            # Unzip
            unzip_to_directory(
                file, 
                extract_path, 
                self.config.pipeline_delete_zip_on_extract
            )
