#!/usr/bin/env bash

set -euo pipefail

expected_python_version_pattern='^Python [0-9]\.[0-9]+'

cd $(dirname "$0")/..

info() {
    echo "* $*"
}

error() {
    echo "Error: $*" >&2
}

check_python() {
    local python
    python=$1
    info "Checking Python binary: $python"
    info "Expecting it is executable and with -V it outputs a version number"
    [ -x "$python" ] && "$python" -V | grep -Eq "$expected_python_version_pattern"
}

python=${1?Usage: $0 path/to/very/specific/version/of/python}
info "Checking Python path pattern: $python"

if ! [[ $python =~ .*/python[0-9]+\.[0-9]+$ || $python =~ .*/python@[0-9]+\.[0-9]+/.*/python[0-9] ]]; then
    error "Python path does not match pattern: .*/python[0-9]+\.[0-9]+$"
    error "Got: $python"
    exit 1
fi

if ! check_python "$python"; then
    error "Output of $python -V does not match expected pattern: $expected_python_version_pattern"
    error "Got: $("$python" -V)"
    exit 1
fi

virtualenv=./virtualenv
if check_python "$virtualenv"/bin/python; then
    info "Virtual environment '$virtualenv' exists and looks ok. Exit."
    exit
fi

set -x

"$python" -m venv "$virtualenv"

./pip.sh install --upgrade pip

./pip.sh install -r requirements.txt
