# DMARCReporting ![Build Status](https://github.com/mozaicworks/DMARCReporting/actions/workflows/build.yml/badge.svg?event=push)

This is a simple tool that displays the errors from a bunch of DMARC reports. It's meant to simplify the job of figuring out DMARC errors.

This is very much a work in progress, use only for tests! Feedback and pull requests are welcome.

## How to use

* Download all zipped DMARC reports to the `samples` folder
* Run the script

Two reports are created in the `reports` folder, one for DKIM errors and one for SPF errors.

## Prerequisites

This is a bash script, tested on Ubuntu. It requires `unzip` and `xmllint`. Install them on Ubuntu using:

~~~~
sudo apt install unzip
sudo apt install libxml2-utils
~~~~

## Known Issues

* The reports are not very informative for now
* Opening a report in a browser gives a formatting error

## Development Notes

This tool was started by Alex Bolboaca, with a clear goal: allow easier processing DMARC reports received by email. Alternate tools exist, but they are meant for enterprises, meaning they are either expensive or use a lot of infrastructure.

The main goal is to see a report of email failures to allow investigation. Therefore, this tool should be minimalistic, extracting the minimum necessary information and requiring a minimum infrastructure.

While it's possible to deploy it as a cloud function through a later development of a Docker container, it should also allow running it locally after obtaining the DMARC zipped reports in some way.
