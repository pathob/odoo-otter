from __future__ import print_function
import sys
from pathlib import Path

from otter.const import OTTER_DIR, OTTER_CFG

# Paths must be initiated here to be available for all modules
Path(OTTER_DIR).mkdir(parents=True, exist_ok=True)
Path(OTTER_CFG).touch(exist_ok=True)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# from otter.otter import main

# __all__ = ['main']
