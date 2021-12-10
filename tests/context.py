# To give the individual tests import context, create `tests/context.py`
# See The Hitchhiker's Guide to Python - Structuring Your Project
# https://docs.python-guide.org/writing/structure/
#
# Within the individual test modules, import the module like so:
# ```
# from .context import sample
# ```

import os
import sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import DMARCReporting  # noqa: E402, F401
