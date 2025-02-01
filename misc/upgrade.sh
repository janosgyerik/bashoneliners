#!/usr/bin/env bash

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

# Restart Django site
touch ../tmp/restart.txt

# Export static site to ../public/
./manage.sh distill-local ../public/ --force
cp ../public.bak/goo* ../public.bak/.htaccess ../public/
