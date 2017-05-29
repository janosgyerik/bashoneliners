#!/bin/sh

cd $(dirname "$0")/..

virtualenv=./virtualenv
test -d $virtualenv || python -m venv $virtualenv

requirements=requirements.txt
test -f $requirements && ./pip.sh install -r $requirements
