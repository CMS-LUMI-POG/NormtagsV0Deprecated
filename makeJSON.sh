#!/bin/bash

# This script simply runs the Python parser to determine valid
# lumisections for each luminometer in turn.

fillNumber=$1

echo "fillNumber = $fillNumber"
echo "-----"

for i in bcm1f hfoc pltzero; do
    brilcalc lumi -f $fillNumber --type $i -b "STABLE BEAMS" --byls -o output.csv
    python ./bestlumi.py output.csv
    echo "-----"
done