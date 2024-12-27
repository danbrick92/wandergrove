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
1) Miniconda or Anaconda Installed
2) (optional) QGIS Installed locally (for visualization of data)

### Build Environment
I have supplied a conda env in ```env/gis_env.yml```. 
You can import this and run it in your conda env with ```conda env create -f gis_env.yml```

This will take a few minutes to create the conda enviroment.

### Validate
Make sure you have activated the environment. YOu can do this with ```conda activate gis_env```

In the running container, to validate, run: ```make test-env```
If you see "✅ **All libraries passed validation successfully!**" that means it worked!

Do the same by opening test.ipynb. Select the gis kernel, and make sure it outputs a series of points at the end.

## How-to-Guide
### Running Data Pipeline
#### Natural Earth
Take a look at the arguments specified in 'src/run_data_pipeline.py'

When you are ready, run ```python src/run_data_pipeline.py``` with the arguments you need.
This will scrape Natural Earth's website, download zip files, and extract them. This takes time.

Using the notebook 'src/notebooks/natural_earth_map_layering.ipynb', you can visualize and mess with layering.
