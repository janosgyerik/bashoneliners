# Bash One-Liners graphics generator Makefile v0.1
# http://bashoneliners.com/
#
# Copyright 2012, Janos Gyerik
# http://bashoneliners.com/LICENSE
# 
# Note: requires ImageMagick to resize images
#
src_dir:=src
icons_dir:=../media/icons

names:=$(patsubst $(src_dir)/%,%,$(wildcard $(src_dir)/*.png $(src_dir)/*.jpg))
icons_target:=$(patsubst %,$(icons_dir)/%,$(names))
launchpad_target:=launchpad/icon.png launchpad/logo.png launchpad/brand.png

default: all

lp launchpad: $(launchpad_target)

icons: $(icons_target)

all: launchpad icons

launchpad/icon.png: $(src_dir)/square.png
	@mkdir -p $(@D)
	convert -geometry 14x $< $@
	identify $@

launchpad/logo.png: $(src_dir)/square.png
	@mkdir -p $(@D)
	convert -geometry 64x $< $@
	identify $@

launchpad/brand.png: $(src_dir)/square.png
	@mkdir -p $(@D)
	convert -geometry 192x $< $@
	identify $@


# eof
