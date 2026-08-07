from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, UTC
from pathlib import Path
import aiofiles
import httpx
from utils.base_handler import BaseHandler


@dataclass
class DownloadObject:
    url: str
    filename: str
    path: Path
    timeout: float = 10.0
    mode: str = "wb"


class BaseDownloadHandler(BaseHandler, ABC):
    async def run_handler(self) -> None:
        return await self._download()

    async def _download(self) -> None:
        download_objects = self._get_download_objects()
        source_name = self._get_source_name()

        self.log("Downloading objects", details={"n": len(download_objects), "source": source_name})
        for download in download_objects:
            BaseDownloadHandler._mkdir_download_parent_path(download.path)

            self.log("Downloading", details={"path": str(download.path), "url": download.url, "source": source_name})
            await BaseDownloadHandler.simple_download(download_obj=download)

        self.log("Completed downloading objects", details={"source": source_name})

    #######################################################################################
    # Implement these
    #######################################################################################
    @abstractmethod
    def _get_download_objects(self) -> list[DownloadObject]: ...

    @abstractmethod
    def _get_source_name(self) -> str: ...

    #######################################################################################
    # Pathing
    #######################################################################################
    def _generate_download_path(self, filename: str) -> Path:
        dt = datetime.now(tz=UTC)
        dt_str = dt.strftime(self.config.datetime_fmt)
        return self.config.raw_data_path.joinpath(self._get_source_name(), dt_str, filename)

    @staticmethod
    def _mkdir_download_parent_path(download_path: Path) -> None:
        parent_dir = download_path.parent
        parent_dir.mkdir(parents=True, exist_ok=True)

    #######################################################################################
    # Download routing
    #######################################################################################
    @staticmethod
    async def simple_download(download_obj: DownloadObject) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.get(download_obj.url, timeout=download_obj.timeout)
            response.raise_for_status()

        async with aiofiles.open(download_obj.path, mode=download_obj.mode) as f:
            await f.write(response.content)
