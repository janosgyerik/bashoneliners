# Bash One-Liners graphics generator Makefile v0.1
# https://bashoneliners.com/
#
# Copyright 2012, Janos Gyerik
# https://bashoneliners.com/LICENSE
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

$(icons_dir)/square.png: $(src_dir)/square.png
	@mkdir -p $(@D)
	convert -geometry 14x $< $@
	identify $@

gource: gource/gource.webm

gource/gource.webm: gource/gource.ppm
	ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i $< -vcodec libvpx -b 10000K $@
	> $<
	touch $@
	rm -f opsnr.stt

gource/gource.ppm:
	mkdir -p gource
	gource --file-idle-time 0 --seconds-per-day .5 -640x480 -o $@


# eof
