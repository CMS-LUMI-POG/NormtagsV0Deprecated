## Normtags

To set environment use:
   
   `source brilcalc_env.sh`

###makeValidNT.py

This script takes the csv-style output of brilcalc and produces a normtag that is valid for all of those lumi sections.  
This is an example to get input from brilcalc:

`brilcalc lumi  -f 4266 --normtag hfoc16v3c -o hfoc16v3c_4266_test.csv --output-style csv --byls`

`brilcalc lumi  -f 4266 --normtag pltzerov2 -o pltzero15v2_4266_test.csv --output-style csv --byls`
   

Finally to make the valid normtag files:

`python makeValidNT.py -i hfoc16v3c_4266_test.csv -o normtag_hfoc16v3c_4266.json -n hfoc16v3c`

`python makeValidNT.py -i pltzero15v2_4266_test.csv -o normtag_pltzerov2_4266.json -n pltzerov2`


###makeCompositeNT.py
To combine normtag text files (any normtag files... not just the type from makeValidNT), one can input a 
list of normtag files in ranked order to makeCompositeNT.py.  The output will be a normtag file that 
is valid for all lumi sections where at least one of the input normtags has coverage.

   `python makeCompositeNT.py -n normtag_pltzerov2_4266.json,normtag_hfoc16v3c_4266.json -o normtag_4266_test.json`


##Populating normtag_BRIL.json and individual luminometer procedure

This document describes the current procedure used for updating the normtag files. Note that this is written
with reference to the 2016 procedure, but presumably in 2017 the normtags and
directory will change, so you'll need to update that appropriately.

First, make sure your brilconda environment is set up properly (which should be already done in the .bashrc
file if you're using the cmsbril account) and go to public/2016normtags.  One can use brilcalc_env.sh as above.

Then, for each fill (where #### denotes the fill number):

1) First, use lumiValidate to make a plot of the luminosity for the fill:

`python ../validation/lumiValidate.py -b "STABLE BEAMS" -f #### --normtag bcm1f16v1 pltzero16v3 hfoc16v3b`

Take a look at the plots to see if there are any places where a luminometer drops out or experiences any
strange steps or spikes. In particular, it's a lot easier to see steps in the ratio plot; zoom in on the ratio
plot to make sure that you can see even small steps.

Be aware that lumiValidate uses the first luminometer in the list as the reference luminometer for which LSes
are present, and may behave unexpectedly if that luminometer is missing LSes in the middle of the fill. That's
why it's usually best to put BCM1F first, since it's much less likely than the other two (at least for 2016)
to be missing entirely during a run. But if it is for whatever reason, then you may need to use one of the
other luminometers as the first argument in order to get sensible results.

If there are any sections for which a luminometer looks bad, you'll need to invalidate those sections. See if
you can get more information from the elog or contact the responsible expert to see if there is a known cause,
and note the affected LSes.

2) Get the lumisections for which data is in the lumiDB:

`./makeJSON.sh ####`

This simply runs through the three luminometers and for each of them, runs brilcalc to see which LSes have
data for that luminometer, and then invokes the (somewhat misleadingly named) script bestlumi.py to convert
that information into a JSON file suitable for including into the normtags.

Note that bestlumi.py is responsible for converting the luminometer name into the normtag name, so if the
latest normtag is updated, you will need to change that in bestlumi.py.

Note that BCM1F is gated on the actual beam presence, so it will always end when the fill actually ends. For
the other two, there may be some stray lumisections after the actual end of fill before the STABLE BEAMS flag
is cleared. In general you should just remove these and go with the end reported by BCM1F. If there are any
doubts go to the WBM page for the run and then look at the LumiSections table to see when the actual end of
fill is.

THIS ONLY TELLS YOU WHICH LUMINOMETERS ACTUALLY HAVE DATA, NOT ANYTHING ABOUT THE QUALITY OF THAT DATA. It's
your responsibility to remove sections where the data is known to be bad, which hopefully you discovered in
step 1.

3) Insert the data into the normtag files.

emacs normtag_fills.csv normtag_BRIL.json normtag_pltzero.json normtag_hfoc.json normtag_bcm1f.json &
(or use the text editor of your choice)

For the individual luminometers, just insert the output from makeJSON after removing any sections that you
identified as bad. For normtag_BRIL.json, insert the results for the luminometer that was determined to be
best for that fill, and if there are any missing LSes for whatever reason, substitute in the next luminometer
on the priority list.

Finally, record what you did in normtag_fills.csv: put in the fill number, the luminometer order, and any
notes about bad periods (or anything else that needs noting).

4) CHECK YOUR WORK!

It's very easy to forget a comma when you're editing these files, which will break normtag_BRIL.json and make
the people who depend on it very unhappy. Better to check before you release it!

The most thorough way to check is simply to actually use normtag_BRIL.json with brilcalc:

`brilcalc lumi --normtag /afs/cern.ch/user/c/cmsbril/public/2016normtags/normtag_BRIL.json -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/DCSOnly/json_DCSONLY.txt`

If this runs correctly, great! If it throws an error, it's probably because you forgot a comma (or screwed up
the JSON syntax in some other way). Unfortunately the JSON parser that brilcalc uses is not so helpful as far
as errors go, so you can run

`./checkJSONSyntax.py normtag_BRIL.json`

which, if it throws an error, will tell you where the offending line is, which will hopefully help you track
it down.

Of course, even if the syntax is good, it's also possible that you managed to skip a fill entirely, which will
also create problems down the line. For this, I have another validation script:

`./checkMissingRuns.py`

This will check to see if there are any runs in the latest certification JSON not present in the normtag, and
if so, will complain to you about them. Note that the JSON file used is pretty bleeding edge, so for instance
if a fill is still in progress, it may have runs from that fill in it, which obviously will not yet be in the
normtag yet, so that will create errors (which in that case you can safely ignore). In other cases you should
definitely pay attention if this script complains!

Hopefully that covers the basics of this procedure. If you have any questions, drop me a line at my CERN
email.
--Paul Lujan, December 2016


##Basic Git Instructions

Only once--forever.

0. Create your own fork of CMS-LUMI-POG/Normtags (upper right at https://github.com/CMS-LUMI-POG/Normtags)  

Once per local clone

1. Check out the group's version of the tools
    `git clone https://github.com/CMS-LUMI-POG/Normtags`

2. Now, if you want to further release the local changes, the following steps have to be done. Make a remote to your fork 
   
   `git remote add YOURGITUSERNAME git@github.com:YOURGITUSERNAME/Normtags.git`
   
   Make sure that your remote repositoty has been added
   
   `git remote -v`

Per push (commit to the central repo)

3. Checkout a new local branch in which you start to develop/edit files. This is done with
   
   `git checkout -b LOCAL_BRANCHNAME`
   
   The name of LOCAL_BRANCHNAME could be whatever. For the list of available remote (and local) branches, you can simply type `git branch -a`.

4. Make the first push to YOUR remote repository (fork).  To do this, it is necessary at least one file to have been edited/added. Check in your edited/created file(s) and commit with a descriptive comment 
   
   `git add file1 file2`
   
   `git commit -m "file1 and file2 are changed because..."`

5. Now, it is time to push the LOCAL_BRANCHNAME to YOUR fork.
    
    `git push YOURGITUSERNAME LOCAL_BRANCHNAME`
    
    It is also possible to give to the remote repository a different name with
    
    `git push YOURGITUSERNAME LOCAL_BRANCHNAME:NEW_BRANCHNAME`

6. Make a pull request (PR) with your changes. The easiest way is to do it interactively on your github web interface
  
  a) Go to Normtags repository, i.e. https://github.com/YOURGITUSERNAME/Normtags
  
  b) You will see the indication 'New pull request' within the green context; you can click on it
  
  c) In the new screen of 'Comparing changes' there would be four instances, i.e. (BASE FORK, BASE) and (HEAD FORK, COMPARE)
  
  d) Select as BASE FORK "CMS-LUMI-POG/Normtags" and BASE "master"
  
  e) Select as HEAD FORK "YOURGITUSERNAME/Normtags" and COMPARE the branch name that you want to create the pull request for, e.g. the branch that it was created during steps 5-9
  
  f) An automatic message will be created. There should be 'Able to merge. These branches can be automatically merged.' If not the changes that you are trying to push cannot be automatically adapted. Furhter work will be needed, so for that case better communicate with Chris/Jakob on how to proceed
  
  g) If step f has been successful, simply leave a comment if you think the description you added during previous step (in the commit command) is not sufficient, and then push 
  'Create pull request'
  
  h) Not yet finalized! Someone has to review and merge into CMS-LUMI-POG's "master", before you see your nice work be released. Stay tuned and follow the discussion on the pull request page




