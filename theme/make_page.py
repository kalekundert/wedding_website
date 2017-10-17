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
    )


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    html = render_page(args['<path>'])
    print(html)
