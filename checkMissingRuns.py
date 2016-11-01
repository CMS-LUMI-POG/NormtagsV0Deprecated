#!/usr/bin/python

# A quick script to check for any runs that are present in a given
# input JSON file but not present in the normtag file.
# Usage: checkMissingRuns.py <normtag file> <input JSON file>
# The input JSON file, or both, can be omitted, in which case the
# script will use the defaults below.

# IMPORTANT NOTE: This only checks at the run level! No attempt
# is made to compare the consistency of the LSes within a run.

import sys
import json

normtagFileName = "/afs/cern.ch/user/c/cmsbril/public/2016normtags/normtag_BRIL.json"
jsonFileName = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/DCSOnly/json_DCSONLY.txt"

if (len(sys.argv) >= 2):
    normtagFileName = sys.argv[1]

if (len(sys.argv) >= 3):
    jsonFileName = sys.argv[2]

print "Normtag file: "+normtagFileName
print "JSON file: "+jsonFileName

jsonFile = open(jsonFileName, 'r')
parsedJSON = json.load(jsonFile)

normtagFile = open(normtagFileName, 'r')
parsedNormtag = json.load(normtagFile)

# Extract the list of runs from the normtag, since
# it's not quite in a convenient format.
normtagRuns = {}
for line in parsedNormtag:
    normtagRuns.update(line[1])

# Now compare.
for run in sorted(parsedJSON.keys()):
    if run not in normtagRuns:
        print "Run", run, "missing in normtag file!"

