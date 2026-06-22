FROM ghcr.io/astral-sh/uv:0.11.2-python3.12-trixie

USER root
ENV UV_SYSTEM_PYTHON=1
ENV PORT=2718
ENV MARIMO_HOST=0.0.0.0

# Install system dependencies (as root)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    unixodbc-dev \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user and set up /app (as root)
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -m -s /bin/bash user && \
    mkdir -p /app

RUN chown 1000:1000 /app /usr/local/lib/python3.12/site-packages /usr/local/bin

#copy to /, not /app
COPY --chown=1000:1000 requirements.in /requirements.in

RUN uv pip compile /requirements.in -o /requirements.txt && \
    uv pip install --no-cache -r /requirements.txt

WORKDIR /app

USER 1000:1000

# Default command
CMD ["sh", "-c", "marimo edit --no-token --no-skew-protection --port $PORT --host $MARIMO_HOST"]
