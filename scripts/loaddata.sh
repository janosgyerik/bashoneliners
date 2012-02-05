#!/bin/sh

cd $(dirname "$0")/..

default_mod=main
fixtures_dir=./$default_mod/fixtures

loaddata() {
    obj=$1
    test -f $obj && file=$obj || file=$fixtures_dir/$obj.json
    test $file && python manage.py loaddata $file || echo File missing: $file
}

loaddata auth.User 
loaddata HackerProfile
loaddata OneLiner
loaddata Question
loaddata Answer
loaddata AcceptedAnswer

# eof
