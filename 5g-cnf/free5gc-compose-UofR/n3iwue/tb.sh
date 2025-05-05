#!/bin/bash

# Check if at least one argument is provided
if [ $# -eq 0 ]; then
  echo "No command provided."
  echo "Usage: $0 <command>"
  exit 1
fi

input_command="$1"

case $input_command in
  "core up")
    echo "Executing docker-compose.yaml up..."
    docker compose -f docker-compose-core.yaml up
    ;;
  "core down")
    echo "Executing docker-compose.yaml down..."
    docker compose -f docker-compose-core.yaml down
    ;;
  "ran up")
    echo "Executing docker-compose.yaml up..."
    docker compose -f docker-compose-ran.yaml up
    ;;
  "ran down")
    echo "Executing docker-compose.yaml down..."
    docker compose -f docker-compose-ran.yaml down
    ;;
  "ue up")
    echo "Executing docker-compose.yaml up..."
    docker compose -f docker-compose-ue.yaml up
    ;;
  "ue down")
    echo "Executing docker-compose.yaml down..."
    docker compose -f docker-compose-ue.yaml down
    ;;
  "core start")
    echo "Executing docker-compose.yaml up..."
    docker compose -f docker-compose-core.yaml start
    ;;
  "core stop")
    echo "Executing docker-compose.yaml down..."
    docker compose -f docker-compose-core.yaml stop
    ;;
  "ran start")
    echo "Executing docker-compose.yaml up..."
    docker compose -f docker-compose-ran.yaml start
    ;;
  "ran stop")
    echo "Executing docker-compose.yaml down..."
    docker compose -f docker-compose-ran.yaml stop
    ;;
  "ue start")
    echo "Executing docker-compose.yaml up..."
    docker compose -f docker-compose-ue.yaml start
    ;;
  "ue stop")
    echo "Executing docker-compose.yaml down..."
    docker compose -f docker-compose-ue.yaml stop
    ;;
  *)
    echo "Command not recognized."
    ;;
esac