# A Dockerfile that creates an OCI image that can be used to run the
# scripts for static code analysis on the Python code in this repository.
#
# To create the proper image, run `./scripts/setup_podman_images.sh` from
# the top-level directory of this Git repository. The, run scripts such as
# `./scripts/format.sh` to run the commands in the created container.

# Use the "-alpine" Python image because it is 5% of the size of the "normal"
# image. That is, the "-alpine" image is 50 MB when the "normal" image is 1 GB.

# Build pytype as a separate stage in this multi-stage build.
# This reduces the final size of the image by about 1 GB because the
# build toolchain for pytype is only required at build time and can be
# discarded once the build is done
FROM python:3.10-alpine as pytype_build
RUN pip install --no-cache-dir --upgrade pip
RUN apk add --no-cache gcc build-base rust cargo
RUN pip install --no-cache-dir pytype

# Build the final image, only copying the build artifacts (not the entire
# build toolchain) from the pytype build in the previous stage.
FROM python:3.10-alpine

# Copy the pytype compiled artifacts from the previous build stage.
RUN pip install --no-cache-dir --upgrade pip
COPY --from=pytype_build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=pytype_build /usr/local/bin /usr/local/bin
# Install libstdc++, which pytype requires at runtime.
RUN apk add --no-cache libstdc++

# Install required Python dependencies (other than ptype).
RUN pip install --no-cache-dir absl-py pyink pyflakes

# Install bash, for running shell scripts.
# Install cmake, which is required when running some unit tests.
# Install git, which is used to determine ignored files.
RUN apk add --no-cache bash cmake git

# Set /src as the current working directory.
# When the image is used, the root directory for this Git repository needs to be
# bind-mounted at this location.
WORKDIR /src
