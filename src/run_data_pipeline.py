import argparse
from pathlib import Path
from data_pipeline.natural_earth.natural_earth_pipeline import NaturalEarthPipeline
from data_pipeline.natural_earth.natural_earth_config import NaturalEarthConfig


def run_data_pipeline(source: str, extract: str, transform: str, load: str, data_path: str, urls_path: str, zips_path: str) -> None:
    # Get pipeline
    if source == "natural_earth":
        pipeline = NaturalEarthPipeline(NaturalEarthConfig())
    else:
        raise ValueError(f"Source {source} is not supported")
    
    # Run pipeline 
    if extract == "y":
        ## TODO - don't like this way of passing args - should be in arg parser
        kwargs = {
           "data_path": Path(data_path),
        }
        if urls_path != "":
            kwargs["urls"] = pipeline.load_urls(Path(urls_path))
        if zips_path != "":
            kwargs["zips_path"] = Path(zips_path)
        pipeline.extract(**kwargs)
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
    ## TODO - lot of coupling with natural earth. rethink this.
    parser.add_argument("--data_path", "-d", default="data/natural_earth/", help="where should the data be stored")
    parser.add_argument("--urls_path", default="src/data_pipeline/natural_earth/large_urls.txt", help="supply a text file of urls instead of scraping urls")
    parser.add_argument("--zips_path", default="data/natural_earth/10m", help="supply a path to where natural_earth zips are instead of downloading them")
    args = parser.parse_args()
    return vars(args)
    

if __name__ == "__main__":
    args = parse_args()
    run_data_pipeline(**args)
