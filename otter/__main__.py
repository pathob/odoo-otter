import logging
import sys

cfg = deserialize()
loglevel = cfg['loglevel']
logging.basicConfig(level=loglevel)

# logging.basicConfig(
#     level=loglevel,
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     handlers=[
#         logging.StreamHandler(sys.stdout)
#     ]
# )

if not hasattr(sys, 'frozen'):
    import os
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import otter

otter.main()
