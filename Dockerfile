FROM condaforge/miniforge3:latest
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    make \
 && apt-get -y clean \
 && rm -rf /var/lib/apt/lists/*
RUN conda install -y poetry -c conda-forge