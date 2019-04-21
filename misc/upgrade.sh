#!/bin/sh

set -euo pipefail

cd "$(dirname "$0")"/..

unset GIT_DIR
git pull

./pip.sh install -r requirements.txt
./manage.sh collectstatic --noinput

touch ../tmp/restart.txt
