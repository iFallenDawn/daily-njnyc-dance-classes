#!/bin/bash

# Accept output directory as parameter with default to env
OUTPUT_DIR="${1:-env}"

# Create user.env configuration file in the specified directory

# Port calculation based on user ID

if [ $UID -gt 10000 ]; then
  # Use arithmetic calculation for UIDs greater than 10000 (shared dev environment)
  ADJUSTED_UID=$(( ($UID % 10000) + 1000 ))
  _CALCULATED_PORT=$(( ($ADJUSTED_UID - 1000) * 50 + 10001))
  INITIAL_PORT=$((echo $_CALCULATED_PORT))
  FRONTEND_PORT=$INITIAL_PORT
  BACKEND_PORT=$(($INITIAL_PORT + 1))
  COMPOSE_PROJECT_NAME=$USER
else 
  # Use default ports for UIDs 10000 or less (local dev environment)
  ADJUSTED_UID=$UID
  FRONTEND_PORT=3000
  BACKEND_PORT=8000
  COMPOSE_PROJECT_NAME=""
fi

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Generate the user.env file with ports
printf "%s\n" \
    "" \
    "# User Info"\
    "_UID=$UID"\
    "_ADJUSTED_UID=$ADJUSTED_UID"\
    "USER=$USER"\
    "" \
    "# Docker Info"\
    "COMPOSE_PROJECT_NAME=$COMPOSE_PROJECT_NAME"\
    "" \
    "# API Keys"\
    "" \
    "# Service Ports"\
    "FRONTEND_PORT=$FRONTEND_PORT"\
    "BACKEND_PORT=$BACKEND_PORT"\
    "" \
    > "$OUTPUT_DIR/user.env"