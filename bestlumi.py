#!/usr/bin/env python

# A helper script for making the best lumi files. Run this on an
# output file from lumicalc and it will make a JSON snippet containing
# the run/lumisections present in the data. Also substitutes the
# luminometer names with their normtags.

import os, sys, re
import csv
import argparse

get_input_name = lambda base: base

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("basename", help="Input basename") 
    parser.add_argument("--delimiter", default=",", help="The separator for each row's data")

    return parser.parse_args()

def main():
	options = parse_args()
	base_name = options.basename
	input_filename = get_input_name(base_name)

	lastdet=""
	lastrow=""
	firstls=""
	lastls=""
	lastrun=""
	first=True

	with open(input_filename) as csv_input:
		#, \
		#open(output_filename, 'w') as csv_output:
		#reader = csv.reader(csv_input, delimiter=options.delimiter)
		reader = csv.reader(csv_input, delimiter=",")
		for row in reader:
			if len(row)>7 and row[3]=="STABLE BEAMS":
				fr=row[0].split(":")
				run=fr[0]
				fill=fr[1]
				lsls=row[1].split(":")
				ls=lsls[0]
				cmsls=lsls[1]
				thisdet=row[8]
				if thisdet=="PLTZERO":
					thisdet="pltzero16v3"
				if thisdet=="BCM1F":
					thisdet="bcm1f16v1"
				if thisdet=="HFOC":
					thisdet="hfoc16v3b"
				if first and cmsls!="0":
					firstls=ls
					lastls=ls
					lastrun=run
					lastdet=thisdet
					first=False
				elif cmsls !="0" and (run!=lastrun or thisdet !=lastdet or int(ls)!=(int(lastls)+1) ):
					output="[\""+str(lastdet)+"\",{\""+str(lastrun)+"\":[["+str(firstls)+","+str(lastls)+"]]}],"
					#print "[\"",lastdet,"\",{\"",lastrun,"\":[[",firstls,",",lastls,"]]}],"
					print output
					lastrun=run
					lastdet=thisdet
					firstls=ls
				lastls=ls
		output="[\""+str(lastdet)+"\",{\""+str(lastrun)+"\":[["+str(firstls)+","+str(lastls)+"]]}]"
		print output



if __name__ == "__main__":
    main()
