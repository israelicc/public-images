FROM ghcr.io/astral-sh/uv:0.11.2-python3.12-trixie

# Install system dependencies (as root)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user and set up /app (as root)
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -m -s /bin/bash user && \
    mkdir -p /app && \
    chown -R 1000:1000 /app

WORKDIR /app

# Switch to non-root user for all Python operations
USER 1000:1000

# Create venv as user 1000 (owned by user 1000)
RUN uv venv /app/venv

# Set PATH so all commands use venv by default
ENV PATH="/app/venv/bin:$PATH"

# Copy and install dependencies (as user 1000, inside venv)
COPY --chown=1000:1000 requirements.in .
RUN uv pip compile requirements.in -o requirements.txt && \
    uv pip install --no-cache -r requirements.txt

# Download spaCy models (venv python)
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download en_core_web_md

# Default command
CMD ["python"]
