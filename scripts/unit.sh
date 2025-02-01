#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

echo '### oneliners'
./manage.sh test oneliners
