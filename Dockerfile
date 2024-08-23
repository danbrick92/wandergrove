# Use darribas/gds_py as the base image
FROM darribas/gds_py:latest

# Set environment variables for non-interactive installations
ENV DEBIAN_FRONTEND=noninteractive
USER root

# Install Go and GDAL development libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    golang-go \
    pkg-config \
    wget \
    curl \ 
    git \
    build-essential \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Install GDAL and libs
RUN apt-get update && \
    apt-get install -y gdal-bin libgdal-dev libjpeg-dev libtiff-dev

# Set Go environment variables
ENV GOPATH=/go
ENV PATH=$PATH:/usr/local/go/bin:$GOPATH/bin

# Create the Go workspace directory
RUN mkdir -p /go/src /go/bin /go/pkg

# Ensure GDAL bindings are properly set up
ENV CGO_CFLAGS=-I/usr/include/gdal
ENV CGO_LDFLAGS=-L/usr/lib

# Set working directory
WORKDIR /workspace

# Go installs
RUN go mod init gdal
RUN go get github.com/airbusgeo/godal

# Copy code
COPY data /workspace/data
COPY src /workspace/src

# Do not run conda by default
RUN echo "conda deactivate" >> ~/.bashrc

# Run the file
# RUN go run /workspace/src/data-pipeline/sandbox.go

# Expose port for Jupyter Notebook
EXPOSE 8888


# Start with a bash shell by default
CMD ["bash"]