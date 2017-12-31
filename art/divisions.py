#!/usr/bin/env python3


import scipy.misc
import numpy as np

img = scipy.misc.imread('nav_divisions.png')

def find_lines(arr):
    # Get the pixels that are turned on to any degree.
    arr = (arr > 0)

    # Remove consecutive turned-on pixels.
    for i in reversed(range(len(arr) - 1)):
        if arr[i] and arr[i + 1]:
            arr[i+1] = False

    # Return the indices of the good pixels.
    return np.argwhere(arr).flatten()


r = find_lines(img[0,:,0])
g = find_lines(img[0,:,1])
b = find_lines(img[0,:,2]) + 3

ids = [
        'details',
        'travel',
        'lodging',
        'registry',
        'gallery',
        'contact',
]
li_lefts = r[:-1]
li_widths = r[1:] - r[:-1]
a_lefts = g - li_lefts
a_widths = b - g

divisions = zip(ids, li_lefts, li_widths, a_lefts, a_widths)

for id, li_left, li_width, a_left, a_width in divisions:
    print(f'''\
#{id} {{
    left: {li_left}px;
    width: {li_width}px;
}}
#{id} a {{
    left: {a_left}px;
    width: {a_width}px;
}}
#{id} a:hover {{
    background: url('navsprite.png') -{li_left + a_left}px -50px;
}}
#{id} a:active {{
    background: none;
}}
#{id}.current {{
    pointer-events: none;
    cursor: default;
    background: url('navsprite.png') -{li_left}px -100px;
}}

''')

