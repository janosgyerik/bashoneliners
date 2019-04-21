#!/bin/sh

set -euo pipefail

cd "$(dirname "$0")"/..

unset GIT_DIR
git pull

./scripts/install-or-upgrade-requirements.sh
./manage.sh collectstatic --noinput

touch ../tmp/restart.txt
