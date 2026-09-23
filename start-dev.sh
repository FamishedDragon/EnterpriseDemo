#!/bin/bash

# Builds DB docker image
# Runs docker compose to spin up enterprise-api with all deps
# Currently Postgress

# Get directory of currently executing script
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# get root of vcs project [directory containing .git/]
project_root="$(git -C "$script_dir" rev-parse --show-toplevel)"

## Comment this line to skip building DB every time
# Usually not needed as docker-compose will rebuild it for us if needed
# $project_root/build/build-persist.sh

docker-compose -f $project_root/infrastructure/docker-compose.yml down
docker-compose -f $project_root/infrastructure/docker-compose.yml up -d