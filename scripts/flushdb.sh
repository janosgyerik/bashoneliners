#!/bin/sh

test "$IAMDANGEROUS" || {
    echo This script will DELETE all records from some tables.
    echo This script is DANGEROUS!
    echo If you really want to do this, set IAMDANGEROUS env variable to 1,
    echo or run this script like this: IAMDANGEROUS=1 $0
    exit 1
}

cd $(dirname "$0")/..

./manage.py sqlflush | grep oneliners_ | ./manage.py dbshell

# eof
