#!/bin/sh

set -e

cd $(dirname "$0")/..

echo '### oneliners'
./manage.sh test oneliners
