#!/bin/sh

cd $(dirname "$0")

./manage.sh runserver $* --settings bashoneliners.local_settings
