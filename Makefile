docker-build:
	docker build -t gdal-go-pipeline .

# docker-run:
# 	docker run -it --rm -p 8888:8888 gdal-go-pipeline

docker-run:
	docker run -it --rm --name gdal-go-pipeline -p 8888:8888 gdal-go-pipeline /bin/bash

docker-exec:
	docker exec -it gdal-go-pipeline /bin/bash

