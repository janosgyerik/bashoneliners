#!/bin/sh -e

bzr dpush git+ssh://git@github.com/janosgyerik/bashoneliners.git,branch=master
bzr push
bzr push lp:bashoneliners

# eof
