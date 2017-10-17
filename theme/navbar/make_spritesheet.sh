#!/usr/bin/env bash

d=$(dirname $0)
convert \
    $d/sprite_link.png $d/sprite_hover.png $d/sprite_current.png \
    -gravity north -background '#faf5ef00' -extent x50 \
    -append $1
