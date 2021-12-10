#!/usr/bin/env bash

readonly SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

mkdir -p input 
unzip -o "samples/*.zip" -d input/
for f in samples/*.gz; do gunzip -c $f > input/$(basename ${f%.*}); done

mkdir -p reports

xmllint --xpath "/feedback/record/auth_results/spf[contains(result, 'fail')]" input/*.xml >> reports/report-spf.xml
xmllint --xpath "/feedback/record/auth_results/dkim[contains(result, 'fail')]" input/*.xml >> reports/report-dkim.xml

xmllint --xpath "/feedback/record/row/source_ip[../policy_evaluated/disposition = 'reject']" input/*.xml >>reports/dmarc-rejected.xml
xmllint --xpath "/feedback/record/row/source_ip[../policy_evaluated/disposition = 'quarantine']" input/*.xml >>reports/dmarc-quarantined.xml

${SCRIPT_DIR}/bin/DMARCReporting ./input
