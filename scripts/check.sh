#!/bin/sh

cd $(dirname "$0")/..

dirs='bashoneliners oneliners'

echo '### pep8'
pep8 $dirs | grep -v 'line too long'
echo

echo '### pyflakes'
pyflakes $dirs
echo

# eof
