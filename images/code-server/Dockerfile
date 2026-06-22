FROM ghcr.io/linuxserver/code-server:4.123.0

USER root

# system deps (lean)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    bash \
    git \
 && rm -rf /var/lib/apt/lists/*

# Node via NodeSource (mais leve e moderno que apt nodejs default)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt-get install -y nodejs \
 && rm -rf /var/lib/apt/lists/*

# uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
 && ln -sf /root/.local/bin/uv /usr/local/bin/uv \
 && ln -sf /root/.local/bin/uvx /usr/local/bin/uvx

ENV PATH="/root/.local/bin:/root/.cargo/bin:/usr/local/bin:$PATH"

RUN python3 --version && node -v && npm -v && uv --version || true

USER abc