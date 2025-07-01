# Docker Build Process Documentation

This document provides detailed information about the Docker build process for the EDIParse application, including the
multi-stage build process, file copying mechanisms, and known issues.

## Multi-Stage Build Overview

The Dockerfile uses a multi-stage build approach to optimize the final image size and improve security. The build
consists of the following stages:

1. **Base Stage**: Sets up the Red Hat UBI8 minimal image with Python 3.9
2. **OpenAPI Generator Stage**: Generates API endpoints from the OpenAPI specification
3. **Builder Stage**: Installs the application and its dependencies
4. **Test Runner Stage**: Runs the application tests
5. **Service Stage**: Creates the final runtime image

## Stage Details

### Base Stage

```dockerfile
FROM registry.access.redhat.com/ubi8/ubi-minimal:latest AS base

# Install Python 3.9
RUN microdnf install -y python39 python39-pip && \
    microdnf clean all
```

This stage:
- Uses Red Hat UBI8 minimal as the base image for security and compliance
- Installs Python 3.9 and pip
- Cleans up package manager cache to reduce image size

### OpenAPI Generator Stage

```dockerfile
FROM base AS openapi_generator

WORKDIR /tmp/openapi-gen

# Copy OpenAPI specification
COPY docs/ediparse.openapi.yaml ./

# Generate API endpoints from OpenAPI specification
RUN microdnf install -y tar gzip java-11-openjdk && \
    microdnf clean all && \
    # Download OpenAPI generator
    curl -o openapi-generator-cli.jar https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.14.0/openapi-generator-cli-7.14.0.jar && \
    # Run OpenAPI generator in a separate directory to avoid conflicts with existing code
    java -jar openapi-generator-cli.jar generate \
    -p packageName=ediparse.adapters.inbound.rest \
    -i ediparse.openapi.yaml \
    -g python-fastapi \
    -o /tmp/generated-api && \
    # Create the directory structure for the generated files
    mkdir -p /generated/ediparse/adapters/inbound/rest && \
    # Copy all generated files except edifact_parser_api.py
    cp -r /tmp/generated-api/src/ediparse/adapters/inbound/rest/* /generated/ediparse/adapters/inbound/rest/ && \
    # Remove the edifact_parser_api.py file to avoid overwriting the custom version
    rm -f /generated/ediparse/adapters/inbound/rest/apis/edifact_parser_api.py
```

This stage:
- Installs Java 11 for running the OpenAPI generator
- Downloads the OpenAPI generator CLI
- Generates API endpoints from the OpenAPI specification
- Creates a directory structure for the generated files
- Copies the generated files to a specific location
- **Important Note**: Removes the generated `edifact_parser_api.py` file to prevent overwriting the custom implementation

### Builder Stage

```dockerfile
FROM base AS builder

WORKDIR /usr/src/app

# Create virtual environment and install uv
RUN python3.9 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install uv

ENV PATH="/venv/bin:$PATH"

# Copy only necessary files for installation
COPY pyproject.toml LICENSE.txt README.md ./
COPY src src/

# Copy generated API files from openapi_generator stage, excluding edifact_parser_api.py
COPY --from=openapi_generator /generated/ediparse/adapters/inbound/rest/ src/ediparse/adapters/inbound/rest/

# Install application dependencies using uv
RUN uv pip install --no-cache-dir .
```

This stage:
- Creates a Python virtual environment
- Installs the uv package manager for faster dependency installation
- Copies only the necessary files for installation
- Copies the generated API files from the openapi_generator stage
- Installs the application and its dependencies

### Test Runner Stage

```dockerfile
FROM base AS test_runner

WORKDIR /usr/src/app

# Create a new virtual environment for testing
RUN python3.9 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install uv

ENV PATH="/venv/bin:$PATH"

# Copy application code and test files
COPY pyproject.toml LICENSE.txt README.md ./
COPY src src/
COPY tests tests/

# Install dependencies including dev dependencies using uv
RUN uv pip install --no-cache-dir ".[dev]"

# Run tests
RUN uv run -m pytest tests
```

This stage:
- Creates a separate virtual environment for testing
- Copies the application code and test files
- Installs the application with development dependencies
- Runs the tests

### Service Stage

```dockerfile
FROM base AS service

WORKDIR /app

# Set up environment variables
ENV PATH="/venv/bin:$PATH"

# Copy the virtual environment from the builder stage
COPY --from=builder /venv /venv

# Copy only the application code needed for runtime
COPY --from=builder /usr/src/app/src/ediparse ./ediparse

# Copy necessary files for runtime
COPY pyproject.toml LICENSE.txt README.md ./

# Set the entrypoint to run the application
EXPOSE 8000
CMD ["uvicorn", "ediparse.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

This stage:
- Creates the final runtime image
- Copies the virtual environment from the builder stage
- Copies only the necessary application code for runtime
- Exposes port 8000 for the application
- Sets the command to run the application

## Important Notes on File Copying

### Generated API Files

The Dockerfile handles the generation and copying of API files in a specific way to avoid overwriting custom
implementations:

1. The OpenAPI generator generates API endpoints in the `/tmp/generated-api` directory
2. The generated files are copied to `/generated/ediparse/adapters/inbound/rest/`
3. The `edifact_parser_api.py` file is explicitly removed to prevent overwriting the custom implementation
4. In the builder stage, the generated files are copied to `src/ediparse/adapters/inbound/rest/`

### Known Issue: Custom API Implementation Protection

**Important**: The Dockerfile includes a critical step to prevent overwriting custom API implementations:

```dockerfile
# Remove the edifact_parser_api.py file to avoid overwriting the custom version
rm -f /generated/ediparse/adapters/inbound/rest/apis/edifact_parser_api.py
```

This step is necessary because:
1. The project uses a custom implementation of `edifact_parser_api.py` that contains specific business logic
2. The OpenAPI generator would overwrite this custom implementation with a generated version
3. Removing the generated file ensures that the custom implementation is preserved

If this step is removed or modified, it could lead to the loss of custom business logic and cause the application to
malfunction.

## Building and Running the Docker Image

To build the Docker image:

```bash
docker build -t ediparse .
```

To run the Docker image:

```bash
docker run -p 8000:8000 ediparse
```

To build and run with Docker Compose:

```bash
docker compose up --build
```

For more information on Docker deployment, refer to the [Docker Setup](../README.md#docker-setup) section in the README.