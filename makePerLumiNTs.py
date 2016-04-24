#!/usr/bin/env python
#import arrow
import os, sys, re
import csv
import argparse
import numpy as np
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import subprocess
import tempfile
import logging
import atexit
from subprocess import call, Popen, STDOUT
from operator import itemgetter
from itertools import groupby

get_input_name = lambda base: base


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


coords_bad = []
det_type = "None"
detRunLSList = {}

detRunLS = {}
detRunLS_bad = {}

#(Krishna):TODO--DRY
def brilcalc_for_all(fill):
    time_selection = []
    f1 = tempfile.NamedTemporaryFile()
    log.debug("Created temp file name for hfoc: %s", f1.name)

    if fill is not None:
        time_selection += ["-f", str(fill)]

    cmd1 = ["brilcalc", "lumi", "--byls", "-o", f1.name,"--type","hfoc"]
    cmd1 += time_selection
    subprocess.call(cmd1)


    f2 = tempfile.NamedTemporaryFile()
    log.debug("Created temp file name for bcm1f: %s", f2.name)
    cmd2 = ["brilcalc", "lumi", "--byls", "-o", f2.name,"--type","bcm1f"]
    cmd2 += time_selection
    subprocess.call(cmd2)

    f3 = tempfile.NamedTemporaryFile()
    log.debug("Created temp file name for pltzero: %s", f3.name)
    cmd3 = ["brilcalc", "lumi", "--byls", "-o", f3.name,"--type","pltzero"]
    cmd3 += time_selection
    subprocess.call(cmd3)

    #(Krishna): Make plot in-house instead of calling lumiValidate.
    #don't need ratio plot to begin with, and we already have data in scope
    fV = tempfile.NamedTemporaryFile()
    cmdV = ["python","lumiValidate.py", "-o", fV.name]
    time_select = ["-f", str(fill)]
    cmdV += time_select
    # use popen to have it open in background
    # so that one can look at the plot, zoom in and figure out which LS to exclude
    # and then enter the numbers when prompted
    subprocess.Popen(cmdV, stdout=open(os.devnull, "w"), stderr=STDOUT)



    return f1, f2, f3

def main():

    """
    input: FillNo
    - calls lumiValidate.py for visual inspection
    - asks user which detector is being inspected for certification
    - user should enter runNo, LsFrom, LsTo to be excluded

    output:
    (1) recorded_LS.json: for all detectors
    (2) badLS_det_type.json: bad lumi sections for detector of interest
    (3) goodLS_det_type.json: good lumi sections for detector of interest
    """



    parser = argparse.ArgumentParser(description='Create json files for lumi validation')
    parser.add_argument(
        "-f", dest="fill", type=int, help="fill number")

    args = parser.parse_args()

    types = ["hfoc","bcm1f","pltzero"]
    f1,f2,f3 = brilcalc_for_all(args.fill)

    flist = [f1.name,f2.name,f3.name]

    # write available lumi sections for all detectors to a file
    als_file = 'recorded_LS.json'
    f = open(als_file,'w')


    print "\n All Lumi Section Data available for"
    for fname in flist:
        f.write("\n")

        lastdet=""
        lastrow=""
        firstls=""
        lastls=""
        lastrun=""
        first=True
        print "\n",types.pop(0), ":","\n"

        output = []
        input_filename = get_input_name(fname)
        # this section is adapted from  bestlumi.py
        with open(input_filename) as csv_input:
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
                        thisdet="pltzerov1"
                    if thisdet=="BCM1F":
                        thisdet="bcm1fv1"
                    if thisdet=="HFOC":
                        thisdet="hfocv1"
                    if first and cmsls!="0":
                        firstls=ls
                        lastls=ls
                        lastrun=run
                        lastdet=thisdet
                        first=False
                    if cmsls !="0" and (run!=lastrun or thisdet !=lastdet):
                        output="[\""+str(lastdet)+"\",{\""+str(lastrun)+"\":[["+str(firstls)+","+str(lastls)+"]]}],"

                        f.write(output + "\n")
                        #f.write(str(lastdet)+" "+str(lastrun)+" "+str(firstls)+" "+str(lastls)+"\n\n")
                        if (str(lastdet)+"-"+str(lastrun) in detRunLSList):
                            #print "Appending to existing dict: " , lastdet, lastrun
                            detRunLSList[str(lastdet)+"-"+str(lastrun)].extend(range(int(firstls), int(lastls)+1))
                        else:
                            #print "new dict: " , lastdet, lastrun
                            detRunLSList[str(lastdet)+"-"+str(lastrun)] = range(int(firstls), int(lastls)+1)
                        print output

                        lastrun=run
                        lastdet=thisdet
                        firstls=ls
                    lastls=ls
            output="[\""+str(lastdet)+"\",{\""+str(lastrun)+"\":[["+str(firstls)+","+str(lastls)+"]]}]"


            #f.write(str(lastdet)+" "+str(lastrun)+" "+str(firstls)+" "+str(lastls)+"\n\n")
            f.write(output + "\n")

            if (str(lastdet)+"-"+str(lastrun) in detRunLSList):
                #print "Appending to existing dict: " , lastdet, lastrun
                detRunLSList[str(lastdet)+"-"+str(lastrun)].extend(range(int(firstls), int(lastls)+1))
            else:
                #print "new dict: " , lastdet, lastrun
                detRunLSList[str(lastdet)+"-"+str(lastrun)] = range(int(firstls), int(lastls)+1)



            print output
    f.close()


    # detRunLSList = {det_type-runNo==> list_of_all_recorded_LS_for_this_runNo}
    # we now have a dictionary of runNo==>LS for each detector

    print "\n\n"
    print "=======Enter the type of detector you're inspecting============="
    print "=======Options: hfocv1, bcm1fv1, pltzerov1======================"

    det_choices = ["hfocv1","bcm1fv1","pltzerov1"]
    global det_type

    while det_type not in det_choices:
        det_type = raw_input("Enter your choice:  ")


    # Now that we've picked the detector
    # We just need a subset of detRunLSList
    # Get (runNo ==> [LS]) for this detector


    for key, value in detRunLSList.iteritems():
        temp = key.split("-")
        if (temp[0] == det_type):
            detRunLS[temp[1]] = value




    print "Available LS numbers for the detector you picked: \n", detRunLS.keys(),"\n"


    print "\n\n"
    print "================Now Inspect the plot============================="
    print "Enter:==========RunNo LsFrom LsTo================================"
    print "================Press return to enter more bad LS ranges========="

    # detRunLS[runNo]==>LS values for given detector+run
    # we'd like to check if the user enters correct runNO (must be in detRunLSList.keys()
    # and if LsFrom, LsTo exist in detRunLS[runNo]

    while True:
        try:
            run, LsFrom, LsTo = [int(x) for x in raw_input(" ").split()]


            # dummy check
            if (LsFrom <0 or LsTo < 0 or LsFrom > LsTo):
                print "ValueError: Incompatible LS numbers"
                #raise Assertion("ValueError: Incompatible LS numbers")

            # now check if the runNo is there
            if (str(run) in detRunLS):
                # if yes, now check if the LS is there
                if (all(lsChoice in detRunLS[str(run)] for lsChoice in [LsFrom, LsTo])):
                    # append only if good
                    coords_bad.append("[\"" + det_type + "\",{\"" + str(run) + "\":[[" + str(LsFrom) + "," + str(LsTo) + "]]}]")

                    #Keep a record of excluded LS (to get good LS afterwards)
                    if (str(run) in detRunLS_bad.keys()):
                        #print "Appending"
                        detRunLS_bad[str(run)].extend(range(LsFrom,LsTo+1))
                        #print detRunLS_bad
                    else:
                        detRunLS_bad[str(run)] = range(LsFrom,LsTo+1)
                        #print detRunLS_bad

                else:
                    print "ValueError: LsNo not available. Pick LS between ", \
                        detRunLS[str(run)][0], detRunLS[str(run)][-1]
                    #raise Assertion ("ValueError: LsNo not available")
            else:
                print "ValueError: runNo not available"
                #raise Assertion("ValueError: runNo not available")


        except ValueError:
            print 'Enter 3 numerical values with spaces'
        except (KeyboardInterrupt, EOFError):
            print "Bye!"
            break

def exit_handler():
    coord_good_file = 'badLS_' + det_type + '.json'
    f = open(coord_good_file,'w')

    for x in range(0,len(coords_bad) -1 ):
        f.write(coords_bad[x]+",\n")

    f.write(coords_bad[len(coords_bad) - 1]) #we don't want comma for the last guy
    f.close()

    detRunLS_good = {}

    #print detRunLS.keys()
    #print detRunLS_bad.keys()
    for key, val in detRunLS.iteritems():
        if key in  detRunLS_bad.keys():
            detRunLS_good[key] = list(set(detRunLS[key]) - set(detRunLS_bad[key]))
        else:
            detRunLS_good[key] = detRunLS[key]


    coords_good = []
    for key in detRunLS_good.keys():
        #now that we know good LS, group them
        for a, b in groupby(enumerate(detRunLS_good[key]),lambda(i,x):i-x):
            goodGuy = map(itemgetter(1),b)
            coords_good.append("[\"" + det_type + "\",{\"" + str(key) + "\":[[" + str(goodGuy[0]) + "," + str(goodGuy[-1]) + "]]}]")


    coord_good_file = 'goodLS_' + det_type + '.json'
    f = open(coord_good_file,'w')
    for x in range(0,len(coords_good) -1 ):
        f.write(coords_good[x]+",\n")
    f.write(coords_good[len(coords_good) - 1]) #no commas for the last guy. Aww.
    f.close()

#TODO: convert all lists to arrays.

atexit.register(exit_handler)


if __name__ == "__main__":
    main()
