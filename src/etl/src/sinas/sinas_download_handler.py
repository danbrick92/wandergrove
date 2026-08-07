from utils.base_download_handler import BaseDownloadHandler, DownloadObject


class SinasDownloadHandler(BaseDownloadHandler):
    def _get_source_name(self) -> str:
        return "sinas"

    def _get_download_objects(self) -> list[DownloadObject]:
        return [
            DownloadObject(
                url="https://zenodo.org/records/18220953/files/SInAS_3.1.1.csv?download=1",
                filename="SInAS_3.1.1.csv",
                path=self._generate_download_path("SInAS_3.1.1.csv"),
                timeout=20.0,
                mode="wb",
            )
        ]
