#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"/..

./pip.sh install --upgrade pip
./scripts/install-or-upgrade-requirements.sh
./manage.sh collectstatic --noinput
./manage.sh migrate

# Restart Django site
touch ../tmp/restart.txt

# Export static site to ../public/
./manage.sh distill-local ../public/ --force

# Prepare updated site content in a dedicated offline directory.
staging=tmp/distill-staging
rm -fr "$staging"
./manage.sh distill-local "$staging"
cp ../public.bak/goo* ../public.bak/.htaccess "$staging"

# Replace production site with the ready staging site.
rm -fr ../public.old
mv ../public ../public.old
mv "$staging" ../public

rm -fr ../public.old
