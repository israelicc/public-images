FROM ghcr.io/israelicc/images_maker/analytics-db:latest

WORKDIR /

USER root

COPY --chown=1000:1000 requirements_ml.in .
RUN uv pip compile requirements_ml.in -o requirements_ml.txt && \
    uv pip install --no-cache -r requirements_ml.txt

USER 1000:1000
WORKDIR /app

# Default command
CMD ["sh", "-c", "marimo edit --no-token --no-skew-protection --port $PORT --host $MARIMO_HOST"]
