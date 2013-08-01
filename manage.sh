#!/bin/sh

cd $(dirname "$0")

projectname=$(basename $PWD)
virtualenv=~/virtualenv/$projectname/bin/activate
test -f $virtualenv && . $virtualenv

#env=$1; shift

if test $# = 0; then
    python manage.py help
else
    #python manage.py $* --setting=local_settings.$env
    python manage.py $*
fi
