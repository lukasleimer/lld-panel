#!/bin/bash

# LLD Panel - Container Entrypoint
#
# Orchestrates the startup sequence for the Django application:
# 1. Verifies environment configuration
# 2. Applies database migrations
# 3. Collects static files
# 4. Validates Django configuration
# 5. Starts Gunicorn application server
#
# All steps must succeed - any failure stops the container (set -e)

set -e

# =============================================================================
# Logging Functions
# =============================================================================

log_info() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1"
}

log_error() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1" >&2
}

# =============================================================================
# Startup Sequence
# =============================================================================

log_info "═════════════════════════════════════════════════════════════════"
log_info "Starting LLD Panel (Django Application)"
log_info "═════════════════════════════════════════════════════════════════"

# Step 1: Apply database migrations
# Note: Database connectivity must be established by the time this runs.
#       (managed by docker-compose or container orchestration in lld-infrastructure)
log_info "Applying database migrations..."
python manage.py migrate --noinput
log_info "✓ Database migrations applied"

# Step 2: Collect static files
# Gathers all static files (CSS, JS, admin assets) into staticfiles/ directory
# for serving by reverse proxy in production
log_info "Collecting static files..."
python manage.py collectstatic --noinput
log_info "✓ Static files collected"

# Step 3: Validate Django configuration
# Runs Django's system checks to detect configuration issues early
log_info "Running Django system checks..."
python manage.py check --deploy
log_info "✓ Django configuration valid"

# Step 4: Start Gunicorn application server
# - Binds to 0.0.0.0:8000 (accessible from reverse proxy)
# - 4 workers for concurrent request handling
# - Logs to stdout/stderr for container log capture
# - exec: replaces shell process with Gunicorn (PID 1 for proper signal handling)
log_info "───────────────────────────────────────────────────────────────"
log_info "Starting Gunicorn application server..."
log_info "───────────────────────────────────────────────────────────────"

# Gunicorn configuration via environment variables
GUNICORN_BIND=${GUNICORN_BIND:-0.0.0.0:8000}
GUNICORN_WORKERS=${GUNICORN_WORKERS:-3}
GUNICORN_TIMEOUT=${GUNICORN_TIMEOUT:-120}

exec gunicorn config.wsgi:application \
    --bind "$GUNICORN_BIND" \
    --workers "$GUNICORN_WORKERS" \
    --worker-class sync \
    --worker-tmp-dir /dev/shm \
    --timeout "$GUNICORN_TIMEOUT" \
    --keep-alive 5 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --forwarded-allow-ips="*"
