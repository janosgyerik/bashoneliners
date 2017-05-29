#!/bin/bash

set -e

cd $(dirname "$0")/..
. scripts/include.sh

# directories to scan for coding style violations
dirs=${apps[@]}

# E121 continuation line indentation is not a multiple of four
# E123 closing bracket does not match indentation of opening bracket's line
# E126 continuation line over-indented for hanging indent
# E128 continuation line under-indented for visual indent
# E501 line too long > 79 characters
echo '###' pep8 for: $dirs
pep8 $dirs | grep -v \
    -e E121 \
    -e E123 \
    -e E126 \
    -e E128 \
    -e E501 || :
echo

echo '###' pyflakes for: $dirs
pyflakes $dirs || :
echo
