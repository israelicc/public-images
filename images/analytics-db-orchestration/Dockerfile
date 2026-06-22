FROM ghcr.io/israelicc/public-images/analytics-db-ai:latest

USER root

# Copy requirements and install Dagster packages
COPY --chown=1000:1000 requirements.in /requirements.in
RUN uv pip compile /requirements.in -o /requirements.txt && \
    uv pip install --no-cache -r /requirements.txt

# Copy start script and workspace config
COPY --chown=1000:1000 start.sh /start.sh
COPY --chown=1000:1000 workspace.yaml /opt/workspace.yaml
COPY --chown=1000:1000 definitions.py /opt/definitions.py

# Create /opt directory if it doesn't exist and set permissions
RUN mkdir -p /app/cronjobs /app/.dagster_home && \
    chown -R 1000:1000 /app/cronjobs /app/.dagster_home

COPY --chown=1000:1000 dagster.yaml /app/.dagster_home/dagster.yaml

# Make start script executable
RUN chmod +x /start.sh

ENV DAGSTER_HOME=/app/.dagster_home

# Expose webserver port
EXPOSE 3000

USER 1000:1000

# Default command to start both daemon and webserver
CMD ["/start.sh"]
