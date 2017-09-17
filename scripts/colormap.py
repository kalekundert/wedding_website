#!/usr/bin/env python3

"""\
Given the left coordinate and the width of a firework, return its color.

Usage:
    colormap.py <left> <width>

"""

import sys
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize, LinearSegmentedColormap

center = lambda l,w: l + w/2
leftmost = center(-6.625, 70.744)
rightmost = center(496.286, 58.573)

norm = Normalize(leftmost, rightmost, clip=True)
colors = LinearSegmentedColormap.from_list(
        'stamp_pad', [
            (r/255, g/255, b/255)
            for r,g,b in [
                ( 75,  51, 106),
                (125,  35,  60),
                (170,  29,  48),
                (210,  39,  44),
                (245,  73,  40),
                (247, 147,  38),
                (245, 190,  35),
                ( 68, 160,  90),
                ( 27,  91,  68),
                ( 49, 140, 157),
                ( 75, 155, 212),
                ( 48,  57, 115),
            ]
])
f = ScalarMappable(norm, colors)

if len(sys.argv) == 1:
    while True:
        query = center(*map(float, input("<left> <width>: ").split()))
        r,g,b,a = f.to_rgba(query)
        print(f"{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}FF")

else:
    query = center(float(sys.argv[1]), float(sys.argv[2]))
    r,g,b,a = f.to_rgba(query)

print(f"{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}FF")



