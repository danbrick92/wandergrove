import geopandas as gpd
import fiona
import shapely
import pyproj
import rtree

print("GeoPandas version:", gpd.__version__)
gdf = gpd.read_file('data/natural_earth/1_to_50m_physical/ne_50m_geography_regions_polys.shp')
gdf.plot()