__version__ = "0.1.1"

import argparse
from DMARCReporting.cli import CLI


def main():
    cli = CLI()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source_dir", type=str, help="directory containing dmarc reports as .zip files"
    )
    parser.add_argument(
        "-c", dest="csv_output_file", type=str, help="csv output file", default=None
    )
    parser.add_argument(
        "-a",
        dest="get_all",
        action="store_true",
        help="process all records - including successful",
    )
    args = parser.parse_args()

    cli.execute(
        args.source_dir, csv_output_file=args.csv_output_file, show_all=args.get_all
    )
