from abc import ABC, abstractmethod
import os
from pathlib import Path
from utils.base_handler import BaseHandler
from utils.raw_object import RawObject


class BaseLoadHandler(BaseHandler, ABC):
    async def run_handler(self) -> None:
        return await self._load()

    async def _load(self) -> None:
        raw_objects = self._get_raw_objects_with_paths()
        print(raw_objects)

    def _get_raw_objects_with_paths(self) -> list[RawObject]:
        source = self._get_source_name()
        source_path = self.config.raw_data_path.joinpath(source)

        not_found = self._get_raw_objects()
        found: list[RawObject] = []

        # Go from latest to oldest to find each file specified
        date_paths: list[Path] = [dt for dt in source_path.glob("*") if dt.is_dir()]
        date_paths.sort(key=os.path.getmtime, reverse=True)

        for dt in date_paths:
            for f in not_found:
                path = dt.joinpath(f.filename)
                if not path.is_file():
                    continue
                f.path = path
                found.append(f)
                not_found.remove(f)
                if len(not_found) == 0:
                    break
            if len(not_found) == 0:
                    break

        if len(not_found) > 0:
            raise FileNotFoundError(f"Unable to find files: {[f.filename for f in not_found]}")

        return found

    #######################################################################################
    # Implement these
    #######################################################################################
    @abstractmethod
    def _get_raw_objects(self) -> list[RawObject]: ...

    @abstractmethod
    def _get_source_name(self) -> str: ...
