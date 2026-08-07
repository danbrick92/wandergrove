from pathlib import Path


BASE_PATH = Path("/", "Users", "danielbrickner", "data")
URL = "https://zenodo.org/records/18220953/files/SInAS_Workflow_Manual_vs2.0.pdf?download=1"
SOURCE = "globi"
FILENAME = "SInAS_3.1.1.csv"


def get_file() -> Path:
    source_dir = Path.joinpath(BASE_PATH, SOURCE)
    
    try:
        entries = list(source_dir.glob("*"))
    except Exception as e:
        raise FileNotFoundError(f"could not list entries in {entries}") from e

    entries = [e for e in entries if e.is_dir()]
    entries = sorted(entries, key=lambda p: p.stat().st_mtime, reverse=True)

    target_dir = entries[0]
    file_dir = target_dir.joinpath(FILENAME)

    if not file_dir.exists() or not file_dir.is_file():
        raise FileNotFoundError(f"Cannot find: {file_dir}")
    return file_dir


def read_csv(filepath: Path) -> None:
    pass


def main():
    file_path = get_file()
    print(file_path)
    read_csv(file_path)


if __name__ == "__main__":
    main()
