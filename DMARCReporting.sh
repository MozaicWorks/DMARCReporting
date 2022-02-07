#!/usr/bin/env bash

readonly SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

${SCRIPT_DIR}/bin/DMARCReporting ./samples
