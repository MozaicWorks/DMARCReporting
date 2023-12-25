## 0.3.0 (25 December 2023)

BREAKING CHANGE: Improved file handling causes the report to show the file DMARC RUA report path in the report ([#10](https://github.com/MozaicWorks/DMARCReporting/issues/10)).
Added support for Python 3.12 ([#20](https://github.com/MozaicWorks/DMARCReporting/issues/20)).
Improved the release process to read the version number from the Python module version ([#14](https://github.com/MozaicWorks/DMARCReporting/issues/14)).
Added support for GZip files with trailing garbage ([#18](https://github.com/MozaicWorks/DMARCReporting/issues/18)).
BREAKING CHANGE: Included the DMARC RUA Report date range in the report ([#12](https://github.com/MozaicWorks/DMARCReporting/issues/12)).

## 0.2.1 (30 November 2023)

Fixed the incorrect reporting due to XML tag ordering ([#19](https://github.com/MozaicWorks/DMARCReporting/issues/19) reported by [@yaiqsa](https://github.com/yaiqsa)). Instead of positional tag parsing we now rely on xpath to parse the DMARC RUA XML reports.

## 0.2.0 (31 October 2022)

Summarising report in one large table with an extra column for the report file name ([#15](https://github.com/MozaicWorks/DMARCReporting/pull/15) by [@beda42](https://github.com/beda42)).
Added the email count column ([#15](https://github.com/MozaicWorks/DMARCReporting/pull/15) by [@beda42](https://github.com/beda42)).
Added `-c` flag to generate a CSV output ([#15](https://github.com/MozaicWorks/DMARCReporting/pull/15) by [@beda42](https://github.com/beda42)).
Added `-a` flag to display all records, not only the failing ones ([#15](https://github.com/MozaicWorks/DMARCReporting/pull/15) by [@beda42](https://github.com/beda42)).
Introduced `argparse` for command line argument parsing ([#15](https://github.com/MozaicWorks/DMARCReporting/pull/15) by [@beda42](https://github.com/beda42)).
Introduced `black` for code formatting ([#15](https://github.com/MozaicWorks/DMARCReporting/pull/15) by [@beda42](https://github.com/beda42)).

## 0.1.1 (7 February 2022)

Initial release
