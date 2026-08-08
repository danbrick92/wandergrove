from utils.base_download_handler import BaseDownloadHandler
from utils.raw_object import RawObject


class SinasDownloadHandler(BaseDownloadHandler):
    def _get_source_name(self) -> str:
        return self.config.sinas.source_name

    def _get_raw_objects(self) -> list[RawObject]:
        return self.config.sinas.raw_objects
