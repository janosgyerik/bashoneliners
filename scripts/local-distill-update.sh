#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..
. scripts/include.sh

distill_out=tmp/distill

./manage.sh distill-local "$distill_out" --force
