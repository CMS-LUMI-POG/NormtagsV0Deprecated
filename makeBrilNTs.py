import re
import operator
from operator import itemgetter
from itertools import groupby

# list of json files with goodLS
listFiles = ["goodLS_pltzerov1.json","goodLS_bcm1fv1.json","goodLS_hfocv1.json"]

#(Krishna): Probably could do without allData
allData = []    #det_type, runNo, lsFrom, lsTo
runRange = {}   #runNo ==> LS numbers

# open the files

for file in listFiles:
    with open(file,'r') as f:
        lines = f.readlines()
        for line in lines:
            temp = re.findall('\w+',line)
            if temp:
                allData.append(temp)
                if temp[1] in runRange.keys():
                    runRange[temp[1]].extend(range(int(temp[2]),int(temp[3])+1))
                else:
                    runRange[temp[1]] = range(int(temp[2]),int(temp[3])+1)


# make a unique runNO ==> LS list

uRunLS = {}
for key,val in runRange.iteritems():
    uRunLS[key] = list(set(val))


# create normtag, give higher preference as:
# smaller index==> higher preference
preference = ["pltzerov1","bcm1fv1", "hfocv1"]

perDetType = {}

# Now that we know unique list of LS for each run,
# we go through all the runs (according to preference)
# order, cross the LS used for normtag

for pref in preference:
    perDetType[pref] = []

# perDetType == det_type=>[runNo, LsFrom, LsTo]
for items in allData:
    if items[0] in perDetType.keys():
        perDetType[items[0]].append(items[1:])
    else:
        perDetType[items[0]] = items[1:]


normTag = []

# Now we have allRunLS in uRunLS and per-detector
# runLS in perDetType, we begin generating NormTag files.
# Main idea is to go through det_type in given order
# of preference, and then crossing off LS from uRunLS
# for each run

for ind in range(0,3):
    det_type = preference[ind]
#    print det_type, ind, '\n\n'

    for runLS in perDetType[det_type]:
        #print runLS
        #runLS == [runNo, LsFrom, LsTo]
        runNo, LsFrom, LsTo = runLS[0],runLS[1],runLS[2]

        # LS still to be tagged for this run
        remLS = set(uRunLS[runNo])

        # LS in this det_type+run
        stripLS = set(range(int(LsFrom),int(LsTo)+1))

        # intersection of available LS, this LS
        intersectLS = list(remLS.intersection(list(stripLS)))

        # LS to tag, still
        diffLS = list(remLS - stripLS)

        # update uRunLS with remaining LS to be tagged
        uRunLS[runNo] = diffLS

        # if intersection is non-empty==> tag this range
        if intersectLS:
            normTag.append([det_type, int(runNo),min(intersectLS), max(intersectLS)])
            #print "^LS: ", runNo, intersectLS,'\n',min(intersectLS),  max(intersectLS),'\n'
        else:
            pass


# Now sort normTag, which is a list of lists, by runNo, LsFrom
normTag.sort(key = operator.itemgetter(1,2))


#Finally, create that json file

normtag_file = 'normtagv1' + '.json'
f = open(normtag_file,'w')
for x in range(0,len(normTag) -1 ):
    f.write("[\"" + normTag[x][0] + "\",{\"" + str(normTag[x][1]) + "\":[[" + str(normTag[x][2]) + "," + str(normTag[x][3]) + "]]}]"+",\n")
f.write("[\"" + normTag[len(normTag) - 1][0] + "\",{\"" + str(normTag[len(normTag) - 1][1]) + "\":[[" + str(normTag[len(normTag) - 1][2]) + "," + str(normTag[len(normTag) - 1][3]) + "]]}]" +"\n")
f.close()
