from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class RawObject:
    url: str
    filename: str
    timeout: float = 10.0
    mode: str = "wb"
    path: Path = field(init=False)

    def set_path(self, raw_data_path: Path, source_name: str, dt_str: str) -> None:
        self.path = raw_data_path.joinpath(source_name, dt_str, self.filename)

    def mkdir_download_parent_path(self, path: Path) -> None:
        parent = path.parent
        parent.mkdir(parents=True, exist_ok=True)
