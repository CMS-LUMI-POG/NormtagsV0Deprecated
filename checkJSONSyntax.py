#!/usr/bin/python

# A very simple script to make sure that a JSON
# file is valid.

import json
import sys

f=open(sys.argv[1])
j=json.load(f)
