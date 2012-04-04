#!/bin/sh

test "$IAMDANGEROUS" || {
    echo This script will DROP and recreate some tables.
    echo This script is DANGEROUS!
    echo If you really want to do this, set IAMDANGEROUS env variable to 1,
    echo or run this script like this: IAMDANGEROUS=1 $0
    exit 1
}

cd $(dirname "$0")/..

./manage.py sqlclear oneliners | ./manage.py dbshell
./manage.py syncdb

# eof
