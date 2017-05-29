#!/bin/sh

set -e

cd $(dirname "$0")

./manage.sh runserver $* --settings bashoneliners.local_settings
