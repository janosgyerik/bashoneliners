#!/bin/sh

cd $(dirname "$0")/..

virtualenv=./virtualenv
test -d $virtualenv || virtualenv --distribute $virtualenv

requirements=requirements.txt
test -f $requirements && ./pip.sh install -r $requirements
