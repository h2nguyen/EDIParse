# Use Red Hat UBI8 as base image
FROM registry.access.redhat.com/ubi8/ubi-minimal:latest AS base

# Install Python 3.9
RUN microdnf install -y python39 python39-pip && \
    microdnf clean all

# OpenAPI Generator stage
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

# Builder stage
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

# Test stage (independent from runtime stage)
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

# Runtime stage (minimal and performant)
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
