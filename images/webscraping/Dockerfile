FROM ghcr.io/israelicc/images_maker/analytics-db:latest

USER root

# Install system dependencies for browsers
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    chromium \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install dependencies
COPY --chown=1000:1000 requirements.in /requirements.in
RUN uv pip compile /requirements.in -o /requirements.txt && \
    uv pip install --no-cache -r /requirements.txt

# Install Playwright browsers
RUN playwright install chromium

USER 1000:1000

# Default command
CMD ["python"]
