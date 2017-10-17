#!/usr/bin/env python3

import numpy as np
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LINK_IDS = [
        'events',
        'travel',
        'lodging',
        'registry',
        'gallery',
        'contact',
]


def find_lines(arr):
    # Get the pixels that are turned on to any degree.
    arr = (arr > 0)

    # Remove consecutive turned-on pixels.
    for i in reversed(range(len(arr) - 1)):
        if arr[i] and arr[i + 1]:
            arr[i+1] = False

    # Return the indices of the good pixels.
    return np.argwhere(arr).flatten()

def find_dimensions(path):
    import scipy.misc
    from types import SimpleNamespace

    img = scipy.misc.imread(str(path))
    dims = SimpleNamespace()

    dims.h, dims.w = img.shape[:2]
    dims.li = find_lines(img[-1,:,0])
    dims.a_left = find_lines(img[-1,:,1])
    dims.a_right = find_lines(img[-1,:,2]) + 3
    dims.a_vert = find_lines(img[:,0,0])

    return dims

def render_scss(template, dims):
    import jinja2

    li_lefts = dims.li[:-1]
    li_widths = dims.li[1:] - dims.li[:-1]
    a_lefts = dims.a_left - li_lefts
    a_widths = dims.a_right - dims.a_left
    a_top = dims.a_vert[0]
    a_height = dims.a_vert[1] - a_top

    banner_width = dims.w
    banner_height = dims.h
    columns = zip(LINK_IDS, li_lefts, li_widths, a_lefts, a_widths)

    y_offset = dict(
            banner = 0,
            hover = 50,
            current = 100,
    )

    loader = jinja2.FileSystemLoader(str(SCRIPT_DIR))
    env = jinja2.Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            undefined=jinja2.StrictUndefined,
    )
    return env.get_template(template).render(locals())

def render_css(scss):
    from subprocess import Popen, PIPE

    sass = 'sass', '--scss'
    p = Popen(sass, stdin=PIPE, stdout=PIPE, encoding='utf-8')
    stdout, stderr = p.communicate(scss)

    return stdout


if __name__ == '__main__':

    path = SCRIPT_DIR / 'nav_divisions.png'
    dims = find_dimensions(path)
    scss = render_scss('navbar.scss.jinja', dims)
    css = render_css(scss)

    print(css)


