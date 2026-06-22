#!/bin/bash
set -e

dagster instance migrate

echo "Starting Dagster daemon..."
dagster-daemon run -w /opt/workspace.yaml &
DAEMON_PID=$!

echo "Starting Dagster webserver..."
dagster-webserver -w /opt/workspace.yaml -h 0.0.0.0 -p 3000

wait
