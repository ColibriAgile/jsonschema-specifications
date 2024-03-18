"""
Load all the JSON Schema specification's official schemas.
"""

import json
import os
import sys

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import (  # type: ignore[import-not-found, no-redef]
        files,
    )

from referencing import Resource


def _schemas():
    """
    All schemas we ship.
    """
    # importlib.resources.abc.Traversal doesn't have nice ways to do this that
    # I'm aware of...
    #
    # It can't recurse arbitrarily, e.g. no ``.glob()``.
    #
    # So this takes some liberties given the real layout of what we ship
    # (only 2 levels of nesting, no directories within the second level).

    frozen = '.zip' in __file__.lower()
    if frozen:
        ref = os.path.dirname(__file__.lower().split('.zip')[0])
        cam = os.path.join(ref, r'jsonschema_specifications\schemas')
        for subdir in os.listdir(cam):
            if '.' not in subdir:
                path = os.path.join(cam, subdir, 'metaschema.json')
                with open(path, encoding='utf-8') as json_file:
                    contents = json.load(json_file)
                yield Resource.from_contents(contents)
        return

    for version in files(__package__).joinpath("schemas").iterdir():
        if version.name.startswith("."):
            continue
        for child in version.iterdir():
            children = [child] if child.is_file() else child.iterdir()
            for path in children:
                if path.name.startswith("."):
                    continue
                contents = json.loads(path.read_text(encoding="utf-8"))
                yield Resource.from_contents(contents)
