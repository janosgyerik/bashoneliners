#!/bin/sh

cd $(dirname "$0")/..

echo '### pep8'
pep8 . | grep -v 'line too long'
echo

echo '### pyflakes'
pyflakes .
echo

# eof
