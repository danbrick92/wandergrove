from abc import ABC, abstractmethod
import aiofiles  # type:ignore
import httpx
from utils.base_handler import BaseHandler
from utils.raw_object import RawObject


class BaseDownloadHandler(BaseHandler, ABC):
    async def run_handler(self) -> None:
        return await self._download()

    async def _download(self) -> None:
        raw_objects = self._get_raw_objects()
        source_name = self._get_source_name()

        self.log("Downloading objects", details={"n": len(raw_objects), "source": source_name})
        for download in raw_objects:
            download.set_path(self.config.raw_data_path, source_name, self.context.dt_str)
            download.mkdir_download_parent_path(download.path)

            self.log("Downloading", details={"path": str(download.path), "url": download.url, "source": source_name})
            await BaseDownloadHandler.simple_download(raw_obj=download)

        self.log("Completed downloading objects", details={"source": source_name})

    #######################################################################################
    # Implement these
    #######################################################################################
    @abstractmethod
    def _get_raw_objects(self) -> list[RawObject]: ...

    @abstractmethod
    def _get_source_name(self) -> str: ...

    #######################################################################################
    # Download routing
    #######################################################################################
    @staticmethod
    async def simple_download(raw_obj: RawObject) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.get(raw_obj.url, timeout=raw_obj.timeout)
            response.raise_for_status()

        async with aiofiles.open(raw_obj.path, mode=raw_obj.mode) as f:
            await f.write(response.content)
