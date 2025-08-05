# ── Build dependencies ───────────────────────────────────────────
FROM python:3.10-slim-bookworm AS builder
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Final image ──────────────────────────────────────────────────
FROM python:3.10-slim-bookworm
WORKDIR /app

# Install Chromium & driver for ARM64
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      chromium \
      chromium-driver \
 && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code and configuration
COPY src/ ./src
COPY config.yaml ./config.yaml

# Create data directories and give permissions to botuser
RUN useradd --create-home botuser \
 && mkdir -p /app/data/raw /app/data/processed \
 && chown -R botuser:botuser /app/data

# Switch to unprivileged user
USER botuser

# Disable Python output buffering
ENV PYTHONUNBUFFERED=1

# Entry point
ENTRYPOINT ["python", "-u", "src/bot.py"]
