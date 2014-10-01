#!/bin/bash

cd $(dirname "$0")
. ./virtualenv.sh

pip $*
