from typing import List, Union
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from exceptions.web import NonHttp200ResponseCode


class NaturalEarthWebScraper:
    def __init__(
        self, 
        base_url: str = "https://www.naturalearthdata.com", 
        suffix: str = ".zip",
        contains_filters: List[str] = []
    ) -> None:
        self.base_url = base_url
        self.suffix = suffix
        self.contains_filters = contains_filters

    def scrape(
        self,
        override_url: Union[str, None] = None,
        override_headers: Union[dict, None] = None,
    ) -> List[str]:
        """
        Scrapes the entire Natural Earth website for links to download from.
        Returns a list of urls that contain both self.base_url and end with the suffix
        """
        # Override base url and header if needed
        base_url = (
            self.base_url + "/downloads/" if override_url is None else override_url
        )
        headers = self.__construct_headers(override_headers)
        print(f"Scraping from base_url: {base_url}")

        # Setup crawler
        queue = [base_url]
        visited = {}
        links: List[str] = []

        # Begin BFS
        while len(queue) > 0:
            link = queue.pop()
            visited[link] = None
            print(f"Visiting: {link}")

            # Make request
            try:
                response = self.__request_content(link, headers)
            except NonHttp200ResponseCode as e:
                print(f"Unable to visit {link}. Error: {e}")
                continue

            # Retreive all links
            soup = BeautifulSoup(response.content, "html.parser")
            a_tags = soup.find_all("a", href=True)
            for a_tag in a_tags:
                link = a_tag["href"]
                # Modify links - some links are provided as relative paths
                if not (link.startswith("http") or link.startswith("https")):
                    link = "https://www.naturalearthdata.com" + link
                    
                # Check for superfluous pages
                if "comment-page" in link or "/feed/" in link or "#comment" in link:
                    continue
                    
                # Inventory
                if link.startswith(base_url) and link not in visited:
                    # Ensure fits in filter
                    if min([filt in link for filt in self.contains_filters]) == 0:
                        continue
                    queue.append(link)
                elif link.startswith(self.base_url) and link.endswith(self.suffix):
                    links.append(link)
        return links
    
    def download_file(
        self, 
        link: str, 
        binary: bool,
        path: Path, 
        override_headers: Union[dict, None] = None,
    ) -> None:
        """
        Downloads file from link to specific path.
        Be sure to set the binary flag correctly.
        Creates the parent directories if they don't exist.
        """
        # Ensure the directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
    
        # Get headers & download
        headers = self.__construct_headers(override_headers)
        response = self.__request_content(link, headers)
        
        # Write
        mode = 'wb' if binary else 'w'
        with open(path, mode) as file:
            print(f"Writing file: {path}")
            file.write(response.content)
    
    def __construct_headers(self, override: Union[dict, None]) -> dict:
        """Simply creates default headers or applies override"""
        headers = {
            'Accept': 'application/zip, application/octet-stream', 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36', 
            'Referer': 'https://www.naturalearthdata.com/downloads/'
        }
        if override:
            headers = override
        return headers
    
    def __request_content(self, url: str, headers: dict) -> requests.Response:
        """
        Performs request and raises exception if non-200.
        """
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise NonHttp200ResponseCode(f"Received {response.status_code}")
        return response
