#!/bin/sh -e

cd $(dirname "$0")/..

unset GIT_DIR
git pull

. ~/virtualenv/bashoneliners/bin/activate
./manage.py collectstatic --noinput

touch ../tmp/restart.txt
