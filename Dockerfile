# syntax=docker/dockerfile:1.7
# ============================================================
# Dockerfile for movie-anime-discovery
# Production image: Django + Gunicorn + WhiteNoise + Tailwind
# ============================================================

FROM python:3.13-slim AS base

# --- Environment ---
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=mysite.settings

# --- System dependencies ---
# - curl, ca-certificates: TLS + downloading the Node.js setup script
# - build-essential, libpq-dev: fallback if psycopg2 needs to compile
# - nodejs (from NodeSource): required by django-tailwind to build CSS
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --- Install uv (copy the binary from Astral's official image) ---
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# --- App directory ---
WORKDIR /app

# --- Python dependencies (cached layer) ---
# Copy lockfile + project metadata FIRST so this layer caches
# unless dependencies actually change.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# --- Application code ---
COPY . .

# --- Install the project itself ---
RUN uv sync --frozen --no-dev

# --- Dummy env vars so Django settings.py can import during build ---
# Real values come from Fly secrets at runtime; these get cleared below
# so missing runtime secrets fail fast instead of silently running with junk.
ENV SECRET_KEY="build-time-dummy-key" \
    DATABASE_URL="sqlite:///tmp/build.db" \
    TMDB_TOKEN="build-time-dummy-token"

# --- Tailwind build (production CSS) ---
RUN python manage.py tailwind install \
    && python manage.py tailwind build

# --- Collect static files ---
RUN python manage.py collectstatic --noinput

# --- Clear dummy build-time vars so runtime fails loudly if secrets are missing ---
ENV SECRET_KEY="" \
    DATABASE_URL="" \
    TMDB_TOKEN=""

# --- Non-root user for security ---
RUN useradd --create-home --shell /bin/bash django \
    && mkdir -p /data \
    && chown -R django:django /app /data
USER django

# --- Runtime ---
EXPOSE 8080
  
CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn mysite.wsgi:application --bind 0.0.0.0:8080 --workers 2 --access-logfile - --error-logfile -"]