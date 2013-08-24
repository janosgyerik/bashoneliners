#!/bin/sh

cd $(dirname "$0")

projectname=$(basename $PWD)
virtualenv=~/virtualenv/$projectname
test -d $virtualenv && . $virtualenv/bin/activate || {
    echo virtualenv does not exist: $virtualenv
    echo Create it with: virtualenv --distribute $virtualenv
    exit 1
}

if test $# = 0; then
    python manage.py help
else
    python manage.py $*
fi
