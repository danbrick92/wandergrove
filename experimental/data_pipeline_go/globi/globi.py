from pathlib import Path
from datetime import datetime, timezone
import requests


BASE_PATH = Path("/", "Users", "danielbrickner", "data")
URL = "https://zenodo.org/records/18220953/files/SInAS_Workflow_Manual_vs2.0.pdf?download=1"
SOURCE = "globi"
FILENAME = "SInAS_Workflow_Manual_vs2.0.pdf"


def get_file(path: Path) -> None:
    response = requests.get(URL)

    with open(path, 'wb') as f:
        f.write(response.content)

    print(f"Wrote: {path}")


def get_path(base_path: Path) -> Path:
    dt = datetime.now(tz=timezone.utc)
    dt_str = dt.isoformat()
    return base_path.joinpath(SOURCE, dt_str, FILENAME)


def make_path(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def main():
    path = get_path(BASE_PATH)
    print(path)
    make_path(path.parent)
    get_file(path)


if __name__ == "__main__":
    main()
