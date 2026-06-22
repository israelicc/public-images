# Stage 1: install opencode in clean Node env
FROM node:20 AS node_stage
RUN npm install -g opencode-ai@latest

# Stage 2: your base image
FROM ghcr.io/israelicc/images_maker/analytics-db-orchestration:latest

USER root

# install ONLY node runtime (no npm install here)
RUN apt-get update && apt-get install -y nodejs

# copy opencode from node stage
COPY --from=node_stage /usr/local/lib/node_modules /usr/local/lib/node_modules
COPY --from=node_stage /usr/local/bin /usr/local/bin

ENV PATH="/usr/local/bin:/usr/bin:/bin:/usr/local/lib/node_modules/.bin:$PATH"

# verify
RUN opencode --help

COPY --chown=1000:1000 start.sh /start.sh
RUN chmod +x /start.sh

USER 1000:1000

CMD ["/start.sh"]
