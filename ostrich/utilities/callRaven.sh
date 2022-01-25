#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
tempDir="${SCRIPT_DIR}/temp_out_raven"
mkdir $tempDir
"${SCRIPT_DIR}/Raven.exe" "${SCRIPT_DIR}/Kreischa" -o $tempDir
mv ${tempDir}/* ${SCRIPT_DIR}/.
wait
