#!/bin/bash

set -e

cd $(dirname "$0")
. ./virtualenv.sh

pip $*
