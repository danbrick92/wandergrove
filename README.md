# Wandergrove

# Getting Started with Development

## Prerequesites
1) Python 3.10 or greater installed on your system
2) Miniconda - https://www.anaconda.com/download/success
3) QGIS - https://www.qgis.org/download/ 
4) VS Code Installed with Jupyer Extension 

## Setup Python Environment
### 1 - Create Miniconda Environment
Run: ```conda create -n gis python=3.10 -y```

### 2 - Activate Conda Environment
Run: ```conda activate gis```

### 3 - Install Core Libs
Run: ```conda install -c conda-forge gdal geos fiona shapely rtree pyproj geopandas jupyterlab -y```

### 4 - Set GDAL Env Variable
Go to your Environmental variables.
Create a new System Variable called GDAL_DATA.
Set the value to C:\Users\{your-userid}\miniconda3\envs\gis\Library\share\gdal

### 5 - Validate
Run: ```python test.py```
If it outputs the geopandas version, everything is setup correctly.

Do the same by opening test.ipynb. Select the gis kernel, and make sure it outputs a map of the world at the end.