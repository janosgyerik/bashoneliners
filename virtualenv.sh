#!/bin/sh

virtualenv=$(dirname "$BASH_SOURCE")/virtualenv
if test -d $virtualenv; then
    . $virtualenv/bin/activate
else
    {
    echo Error: virtualenv does not exist: $virtualenv
    echo Create it with: ./scripts/setup.sh
    } >&2
    return 1
fi
