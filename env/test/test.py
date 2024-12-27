import importlib

# List of libraries to test and an example function to check basic functionality
libraries = {
    "cartopy": lambda: __import__('cartopy.crs').crs.PlateCarree(),
    "elevation": lambda: __import__('elevation'),
    "fiona": lambda: __import__('fiona').supported_drivers,
    "folium": lambda: __import__('folium').Map(location=[0, 0], zoom_start=2),
    "gdal": lambda: __import__('osgeo.gdal').gdal.VersionInfo(),
    "geos": lambda: __import__('shapely.geos'),
    "ipykernel": lambda: __import__('ipykernel'),
    "ipython": lambda: __import__('IPython').InteractiveShell(),
    "jupyterlab": lambda: __import__('jupyterlab'),
    "lxml": lambda: __import__('lxml'),
    "mercantile": lambda: __import__('mercantile').tile(0, 0, 1),
    "networkx": lambda: __import__('networkx').Graph(),
    "numpy": lambda: __import__('numpy').array([1, 2, 3]),
    "osmnx": lambda: __import__('osmnx'),
    "pandas": lambda: __import__('pandas').DataFrame({'a': [1, 2, 3]}),
    "pydeck": lambda: __import__('pydeck'),
    "pyproj": lambda: __import__('pyproj').Proj(proj='utm', zone=33, ellps='WGS84'),
    "pysal": lambda: __import__('pysal'),
    "rasterio": lambda: __import__('rasterio'),
    "requests": lambda: __import__('requests').get('https://httpbin.org/get'),
    "rtree": lambda: __import__('rtree'),
    "scikit-image": lambda: __import__('skimage').io,
    "scikit-learn": lambda: __import__('sklearn').__version__,
    "scipy": lambda: __import__('scipy').linalg.inv([[1, 2], [3, 4]]),
    "seaborn": lambda: __import__('seaborn').set_style('darkgrid'),
    "shapely": lambda: __import__('shapely.geometry').geometry.Point(1, 2),
    "tqdm": lambda: list(__import__('tqdm').tqdm(range(10))),
}

# Run tests
failed_libraries = []

print("\n🔍 **Starting validation of libraries...**\n")

for library, test_func in libraries.items():
    try:
        print(f"✅ Testing {library}...", end=" ")
        test_func()
        print("PASSED")
    except Exception as e:
        failed_libraries.append(library)
        print(f"❌ FAILED - {e}")
        
# Special libs
from matplotlib import pyplot as plt
plt.plot([1, 2, 3], [4, 5, 6])
print("✅ Testing matplotlib... PASSED")

import earthpy
print("✅ Testing earthpy... PASSED")

import geopandas
geopandas.read_file("test.shp")

# Print summary of results
if failed_libraries:
    print("\n❌ **The following libraries failed to import or test properly:**")
    for lib in failed_libraries:
        print(f"  - {lib}")
else:
    print("\n✅ **All libraries passed validation successfully!**")

print("\n🎉 **Validation complete.**")
