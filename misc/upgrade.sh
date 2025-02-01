#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

unset GIT_DIR

git fetch releases

branch=$(git rev-parse --abbrev-ref HEAD)
git reset --hard "releases/$branch"

./misc/upgrade-site.sh
