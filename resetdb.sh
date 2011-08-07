#!/bin/sh

./scripts/dumpdata.sh
echo 'drop table main_oneliner;' | ./manage.py dbshell
./manage.py syncdb
./scripts/loaddata.sh

# eof
