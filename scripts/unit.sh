#!/bin/sh -e

cd $(dirname "$0")/..

echo '### main'
./manage.sh test oneliners

# eof
