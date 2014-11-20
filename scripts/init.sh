#!/bin/bash -e

cd $(dirname "$0")/..

virtualenv=$(. ./virtualenv.sh 2>/dev/null; echo $virtualenv)

if test ! -d $virtualenv; then
    echo virtualenv does not exist: $virtualenv
    printf "Create now? [Yn] "
    read answer
    if [ ! "$answer" ] || [[ $answer == [yY]* ]]; then
        virtualenv --distribute $virtualenv || exit 1
    else
        exit 1
    fi
fi

./pip.sh install -r requirements.txt
