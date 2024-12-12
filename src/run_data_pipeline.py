import argparse
from pathlib import Path
from data_pipeline.natural_earth.natural_earth_pipeline import NaturalEarthPipeline
from data_pipeline.natural_earth.natural_earth_config import NaturalEarthConfig


def run_data_pipeline(source: str, extract: str, transform: str, load: str, data_path: str, urls_path: str) -> None:
    # Get pipeline
    if source == "natural_earth":
        pipeline = NaturalEarthPipeline(NaturalEarthConfig())
    else:
        raise ValueError(f"Source {source} is not supported")
    
    # Run pipeline 
    if extract == "y":
        if urls_path != "":
            paths = pipeline.extract(
                data_path=Path(data_path), 
                urls=pipeline.load_urls(Path(urls_path))
            )
        else:
            paths = pipeline.extract(
                data_path=Path(data_path)
            )
        for path in paths:
            print(path)
    if transform == "y":
        pipeline.load()
    if load == "y":
        pipeline.load()    


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", "-s", default="natural_earth", help="note the source you want to perform etl on")
    parser.add_argument("--extract", "-e", default="y", help="y|n run extraction phase")
    parser.add_argument("--transform", "-t", default="n", help="y|n run transform phase")
    parser.add_argument("--load", "-l", default="n", help="y|n run load phase")
    parser.add_argument("--data_path", "-d", default="data/natural_earth/", help="where should the data be stored")
    parser.add_argument("--urls_path", default="src/data_pipeline/natural_earth/large_urls.txt", help="supply a text file of urls instead of scraping urls")
    args = parser.parse_args()
    return vars(args)
    

if __name__ == "__main__":
    args = parse_args()
    run_data_pipeline(**args)
