#!/bin/bash
set -e

echo "Starting OpenCode..."
opencode &
OPENCODE_PID=$!

echo "Starting Dagster daemon..."
dagster-daemon run -w /opt/workspace.yaml &
DAEMON_PID=$!

echo "Starting Dagster webserver..."
dagster-webserver -w /opt/workspace.yaml -h 0.0.0.0 -p 3000 &
WEB_PID=$!

echo "Starting Marimo..."
env -i PATH=$PATH HOME=$HOME HOST=$MARIMO_HOST \
marimo edit --no-token --no-skew-protection --port $PORT --host $MARIMO_HOST &
MARIMO_PID=$!

trap "echo Shutting down...; kill $OPENCODE_PID $DAEMON_PID $WEB_PID $MARIMO_PID" SIGTERM SIGINT

wait -n