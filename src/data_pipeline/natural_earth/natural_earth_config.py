class NaturalEarthConfig:
    # Scraper Settings
    scraper_base_url = "https://www.naturalearthdata.com"
    scraper_suffix = ".zip"
    scraper_sizes = {
        "large": "/10m-",
        "medium": "/50m-",
        "small": "/110m-"
    }
    contains_filters = [      
        scraper_sizes['large'],
    ]
