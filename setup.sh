#!/bin/sh

cd $(dirname "$0")

virtualenv=./virtualenv
test -d $virtualenv || virtualenv --distribute $virtualenv

./pip.sh install -r requirements.txt
