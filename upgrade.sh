#!/bin/sh -e

cd $(dirname "$0")

git pull

./manage.py collectstatic --noinput

touch ../tmp/restart.txt
