#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

./pip.sh install -U -r requirements.txt
