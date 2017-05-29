#!/bin/sh

set -e

cd $(dirname "$0")/..

requirements=requirements.txt

{
    cat << EOF
# Install required python packages using pip:
# pip install -r $requirements
EOF

    ./pip.sh freeze
} > $requirements
