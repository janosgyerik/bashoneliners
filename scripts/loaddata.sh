#!/bin/sh

cd $(dirname "$0")/..

default_mod=oneliners
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
loaddata AlternativeOneLiner
loaddata Tag
loaddata django_openid_auth.Association
loaddata django_openid_auth.Nonce
loaddata django_openid_auth.UserOpenID

# eof
