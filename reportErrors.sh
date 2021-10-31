#!/usr/bin/env bash

#mkdir -p input 
#unzip "samples/*.zip" -d input/

echo "SPF Errors"
xmllint --xpath "/feedback/record/auth_results/spf[contains(result, 'fail')]" input/*.xml

echo "DKIM Errors"
xmllint --xpath "/feedback/record/auth_results/dkim[contains(result, 'fail')]" input/*.xml
