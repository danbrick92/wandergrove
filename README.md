# Wandergrove

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

## Notes
## Tangental Tech

If you're building a web app for GIS:
PostGIS (backend)
GeoServer (data server)
Leaflet.js (frontend)

If you're building desktop tools:
SpatiaLite (local database)
QGIS (desktop GUI)

If you're doing data analysis:
GeoPandas + PostGIS

If you want everything cloud-based:
AWS S3 + Google BigQuery GIS
