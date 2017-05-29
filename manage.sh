#!/bin/bash

set -e

cd $(dirname "$0")
. ./virtualenv.sh

if test $# = 0; then
    python manage.py help
else
    python manage.py $*
fi
