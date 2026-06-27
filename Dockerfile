# LLD Panel - Production Container
# 
# Multi-purpose Dockerfile for containerizing the Django application.
# Configuration and secrets are provided at runtime via environment variables.
#
# Build: docker build -t lld-panel:latest .
# Run:   docker run -e SECRET_KEY=<key> -e DEBUG=False -p 8000:8000 lld-panel:latest

FROM python:3.14-slim

# Environment configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash django

# Set working directory
WORKDIR /app

# Install production dependencies
# Separated into early layer for better cache utilization
COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/production.txt

# Copy application code
COPY src/ src/

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Set permissions
RUN chmod +x /entrypoint.sh && \
    chown -R django:django /app

# Switch to non-root user
USER django

# Expose application port
EXPOSE 8000

# Change to Django application directory (where manage.py is located)
WORKDIR /app/src

# Container entrypoint
# Handles migrations, static file collection, and application startup
ENTRYPOINT ["/entrypoint.sh"]
