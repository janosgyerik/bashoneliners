#!/bin/sh -e

cd $(dirname "$0")/..

unset GIT_DIR
git pull

./manage.sh collectstatic --noinput

touch ../tmp/restart.txt
