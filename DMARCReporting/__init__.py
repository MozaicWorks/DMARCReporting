__version__ = "0.1.1"

import sys
from DMARCReporting.cli import CLI


def main():
    cli = CLI()
    cli.execute(sys.argv[1])
