#!/bin/sh

set -euo pipefail

cd "$(dirname "$0")"/..

unset GIT_DIR

git fetch releases

branch=$(git rev-parse --abbrev-ref HEAD)
git reset --hard "releases/$branch"

./pip.sh install --upgrade pip
./scripts/install-or-upgrade-requirements.sh
./manage.sh collectstatic --noinput
./manage.sh migrate

touch ../tmp/restart.txt
