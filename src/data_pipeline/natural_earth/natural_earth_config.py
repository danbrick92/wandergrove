class NaturalEarthConfig:
    # Scraper Settings
    scraper_base_url = "https://www.naturalearthdata.com"
    scraper_suffix = ".zip"
    scraper_sizes = {
        "large": "/10m-",
        "medium": "/50m-",
        "small": "/110m-"
    }
    pipeline_contains_filters = [      
        scraper_sizes['large'],
    ]
    pipeline_delete_zip_on_extract = False
    pipeline_all_inclusive_zips = [
        "10m_cultural.zip", 
        "10m_physical.zip", 
        "50m_cultural.zip", 
        "50m_physical.zip", 
        "110m_cultural.zip", 
        "110_physical.zip"
    ]

