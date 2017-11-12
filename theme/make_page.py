#!/usr/bin/env python3

"""\
Usage:
    make_page.py <path>
"""

import docopt
from pathlib import Path
from pprint import pprint

ROOT_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT_DIR / 'content'
THEME_DIR = ROOT_DIR / 'theme'
LINK_IDS = [
        'events',
        'travel',
        'lodging',
        'registry',
        'gallery',
        'contact',
]
PAGE_WIDTH = 690 - 2 * 80
MARGIN = 1
SHADOW = 6

def picture_row(*paths):
    from PIL import Image
    from types import SimpleNamespace
    
    images = []

    for name in paths:
        path = CONTENT_DIR / 'pictures' / name
        pixels = Image.open(str(path))

        image = SimpleNamespace()
        image.src = f'pictures/{name}'
        image.full_width, image.full_height = pixels.size
        image.aspect_ratio = image.full_width / image.full_height

        images.append(image)
        
    net_margin = (MARGIN + SHADOW) * (len(images) - 1)
    height = (PAGE_WIDTH - net_margin) / sum(x.aspect_ratio for x in images)

    for i, image in enumerate(images):
        image.height = height
        image.width = image.aspect_ratio * height
        image.margin = MARGIN if i else 0
        image.html = f'<img src="{image.src}" style="width: auto; height: {image.height}px; margin-left: {image.margin}px;"/>'

    return images

def render_page(path):
    import jinja2
    from types import SimpleNamespace

    path = Path(path)
    dirs = ROOT_DIR / 'content', ROOT_DIR / 'theme'
    loader = jinja2.FileSystemLoader(dirs)
    env = jinja2.Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            undefined=jinja2.StrictUndefined,
    )
    return env.get_template(path.name).render(
            ids=LINK_IDS,
            this_page=path,
            page_width=PAGE_WIDTH,
            picture_row=picture_row,
            zip=zip,
    )


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    html = render_page(args['<path>'])
    print(html)
