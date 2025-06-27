# Use Red Hat UBI8 as base image
FROM registry.access.redhat.com/ubi8/ubi-minimal:latest AS base

# Install Python 3.9
RUN microdnf install -y python39 python39-pip && \
    microdnf clean all

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
