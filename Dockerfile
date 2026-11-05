# ==============================================================================
# Multi-Stage Production Dockerfile for Container Virtualization Micro Project
# Base: Python 3.11-slim (Debian Bookworm)
# ==============================================================================

# STAGE 1: Builder stage
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build tools and MySQL client libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt


# STAGE 2: Final runtime container image
FROM python:3.11-slim

LABEL maintainer="Student <student@university.edu>"
LABEL description="Employee Management & Container Virtualization Microproject"
LABEL virtualization.engine="Docker / Kubernetes / Nginx"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install runtime dependencies and curl for Docker HEALTHCHECK
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    netcat-traditional \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy pre-compiled wheels from builder
COPY --from=builder /build/wheels /wheels
COPY --from=builder /build/requirements.txt .
RUN pip install --no-cache /wheels/* && rm -rf /wheels

# Copy application source code
COPY . /app/

# Create non-privileged system user for container security compliance
RUN useradd -u 1001 -m -s /bin/bash appuser && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app && \
    chmod +x /app/docker-entrypoint.sh

# Mount points for shared volumes
VOLUME ["/app/staticfiles", "/app/media"]

# Expose internal Gunicorn application port
EXPOSE 8000

# Docker Healthcheck directive
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# Execute container entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]

