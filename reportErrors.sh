#!/usr/bin/env bash

mkdir -p input 
unzip -o "samples/*.zip" -d input/

mkdir -p reports

xmllint --xpath "/feedback/record/auth_results/spf[contains(result, 'fail')]" input/*.xml >> reports/report-spf.xml
xmllint --xpath "/feedback/record/auth_results/dkim[contains(result, 'fail')]" input/*.xml >> reports/report-dkim.xml
