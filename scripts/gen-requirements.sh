#!/bin/sh -e

cd $(dirname "$0")/..

requirements=requirements.txt

cat << EOF > $requirements
# Install required python packages using pip:
# pip install -r requirements.txt
EOF

./pip.sh freeze >> $requirements
