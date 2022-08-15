# DMARCReporting ![Build Status](https://github.com/mozaicworks/DMARCReporting/actions/workflows/build.yml/badge.svg?event=push)

This is a simple tool that displays the errors from a bunch of DMARC reports. It's meant to simplify the job of figuring out DMARC errors.

This is very much a work in progress, use only for tests! Feedback and pull requests are welcome.

## Install

```bash
pip install DMARCReporting
```

## How to use

* Download all zipped DMARC reports to a `samples` folder
* Execute:
  
  ```bash
  DMARCReporting /path/to/samples
  ```

The tool processes the files one by one:

* unarchives the file on the fly
* parses the DMARC report
* if any DMARC rejection or quarantine or a failing SPF and/or DKIM authentication and/or alignment happens, a report is displayed on the console together with the DMARC report file name.

An example report looks as follows:

```plain
report.xml.gz
Source IP      Source Host                     Payload From (From:)    Envelop From (MAIL FROM)    DMARC    DKIM Align    DKIM Auth    SPF Align    SPF Auth
-------------  ------------------------------  ----------------------  --------------------------  -------  ------------  -----------  -----------  ----------
80.96.161.193  Unknown host                    bellous.com             bellous.com                 none     pass          pass         fail         fail
208.90.221.45  208-90-221-45.static.flhsi.com  bellous.com             calendar.yambo.com          none     pass          pass         fail         pass

report.xml.zip
Source IP      Source Host                     Payload From (From:)    Envelop From (MAIL FROM)    DMARC    DKIM Align    DKIM Auth    SPF Align    SPF Auth
-------------  ------------------------------  ----------------------  --------------------------  -------  ------------  -----------  -----------  ----------
80.96.161.193  Unknown host                    disicious.com           disicious.com               none     pass          pass         fail         fail
208.90.221.45  208-90-221-45.static.flhsi.com  disicious.com           calendar.trumbee.com        none     pass          pass         fail         pass
```

## Run tests

```bash
make install-dev
make test
```

## Development Notes

This tool was started by [Alex Bolboaca](https://twitter.com/alexboly), with a clear goal: allow easier processing DMARC reports received by email. Alternate tools exist, but they are meant for enterprises, meaning they are either expensive or use a lot of infrastructure.

The main goal is to see a report of email failures to allow investigation. Therefore, this tool should be minimalistic, extracting the minimum necessary information and requiring a minimum infrastructure.

While it's possible to deploy it as a cloud function through a later development of a Docker container, it should also allow running it locally after obtaining the DMARC zipped reports in some way.

The current version has been developed mostly by [Thierry de Pauw](https://twitter.com/tdpauw), so all thanks should go to him :).
