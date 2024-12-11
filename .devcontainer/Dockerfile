# Use official Python image as the base image
FROM python:3.10-slim

# Avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies (important for GDAL, PROJ, GEOS)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    libproj-dev \
    libgeos-dev \
    libspatialindex-dev \
    libxml2-dev \
    libxslt1-dev \
    libpq-dev \
    build-essential \
    software-properties-common \
    wget \
    curl \
    unzip \
    ca-certificates \
    python3-dev \
    python3-pip \
    bash \
    git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables to avoid DLL load issues
ENV GDAL_DATA=/usr/share/gdal
ENV PROJ_LIB=/usr/share/proj
ENV PATH="/root/.local/bin:$PATH"

# Install pip and required Python libraries (use conda-like control)
COPY requirements.txt /workspace/
RUN pip install -r /workspace/requirements.txt

# Expose Jupyter port
EXPOSE 8888

# Set the working directory (where your code will be stored)
WORKDIR /workspace

# Copy project files (if any)
COPY . /workspace

# Set default command to keep container running
CMD ["bash"]
