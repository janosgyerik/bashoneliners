#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..
. scripts/include.sh

if ! [ -d "$distill_out" ]; then
  ./scripts/local-distill-update.sh
fi

(cd "$distill_out" && python3 -m http.server 5000)
