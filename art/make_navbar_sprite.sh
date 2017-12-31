#!/usr/bin/env bash

rm navsprite.png
convert \
    nav_link.png nav_hover.png nav_current.png \
    -gravity north -background '#faf5ef00' -extent 543x50 \
    -append navsprite.png  && echo "success" || echo "Error!"
