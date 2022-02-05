#!/usr/bin/env bash

readonly SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

mkdir -p input 
unzip -o "samples/*.zip" -d input/
for f in samples/*.gz; do gunzip -c $f > input/$(basename ${f%.*}); done

${SCRIPT_DIR}/bin/DMARCReporting ./input
