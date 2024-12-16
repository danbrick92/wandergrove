# Wandergrove
![icon](public/icon.png)

The goal of this project is to create a fun strategy game that:

1) Raises climate and environmental awareness
2) Contains several factors that are at odds like overall CO2 emissions, currency, contrarian leaders, etc.
3) Uses real GIS data to inform new climate or environmental events. 
4) Can prompt users to have real impact by donating to charity when they perform an action in game.
    (IE: Reforesting an area might give the user the occassional bump to donate to OneTreePlanted)
    I'd love for this to be localized if possible.

## Current State
This is very much a WIP. I am currently exploring different data sources and building out the GIS pipelines

## Getting Started (Development)
### Prerequesites
1) VS Code Installed
2) Dev Containers extension installed
3) Docker Installed
4) QGIS Installed locally (for visualization of data)

### Build and Run Container
When you open VS Code, the Dev Containers plugin should automatically detect devcontainer folder and ask to reopen in container. This will automatically build and begin running the dev container. 

This will take a few minutes the first time. 

### Validate
In the running container, run: ```make test-env```
If you see "✅ **All libraries passed validation successfully!**" that means it worked!

Do the same by opening test.ipynb. Select the gis kernel, and make sure it outputs a series of points at the end.

## How-to-Guide
### Running Data Pipeline
#### Natural Earth
Take a look at the arguments specified in 'src/run_data_pipeline.py'

When you are ready, run ```python src/run_data_pipeline.py``` with the arguments you need.
This will scrape Natural Earth's website, download zip files, and extract them. This takes time.

Using the notebook 'src/notebooks/natural_earth_map_layering.ipynb', you can visualize and mess with layering.
