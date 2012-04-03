#!/bin/sh

set -e

cd $(dirname "$0")/..

echo '### main'
./manage.py test main

# eof
