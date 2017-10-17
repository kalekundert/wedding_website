#!/usr/bin/env bash

d=$(dirname $0)
convert \
    $d/nav_link.png $d/nav_hover.png $d/nav_current.png \
    -gravity north -background '#faf5ef00' -extent x50 \
    -append $1
