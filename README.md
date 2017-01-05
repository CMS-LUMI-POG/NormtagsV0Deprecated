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



##Basic Git Instructions

Only once--forever.
0. Create your own fork of CMS-LUMI-POG/Normtags (upper right at https://github.com/CMS-LUMI-POG/Normtags)  

Once per local clone
1. Check out the group's version of the tools
    `git clone https://github.com/CMS-LUMI-POG/Normtags`

2. Now, if you want to further release the local changes, the following steps have to be done. Make a remote to your fork 
   `git remote add YOURGITUSERNAME git@github.com:YOURGITUSERNAME/Normtags.git'
   Make sure that your remote repositoty has been added
   `git remote -v'

Per push (commit to the central repo)
3. Checkout a new local branch in which you start to develop/edit files. This is done with
   `git checkout -b LOCAL_BRANCHNAME`
   The name of LOCAL_BRANCHNAME could be whatever. For the list of available remote (and local) branches, you can simply type `git branch -a`.

4. Make the first push to YOUR remote repository (fork).  To do this, it is necessary at least one file to have been edited/added. Check in your edited/created file(s) and commit with a descriptive comment 
   ```
    git add file1 file2  
    git commit -m "file1 and file2 are changed because..." 
   ```	  
5. Now, it is time to push the LOCAL_BRANCHNAME to YOUR fork.
    `git push YOURGITUSERNAME LOCAL_BRANCHNAME`
    It is also possible to give to the remote repository a different name with
    `git push YOURGITUSERNAME LOCAL_BRANCHNAME:NEW_BRANCHNAME`

6. Make a pull request (PR) with your changes. The easiest way is to do it interactively on your github web interface
  
  a) Go to YOUR Normtags repository, i.e. https://github.com/YOURGITUSERNAME/Normtags
  
  b) You will see the indication 'New pull request' within the green context; you can click on it
  
  c) In the new screen of 'Comparing changes' there would be four instances, i.e. (BASE FORK, BASE) and (HEAD FORK, COMPARE)
  
  d) Select as BASE FORK "CMS-LUMI-POG/Normtags" and BASE "master"
  
  e) Select as HEAD FORK "YOURGITUSERNAME/Normtags" and COMPARE the branch name that you want to create the pull request for, e.g. the branch that it was created during steps 5-9
  
  f) An automatic message will be created. There should be 'Able to merge. These branches can be automatically merged.' If not the changes that you are trying to push cannot be automatically adapted. Furhter work will be needed, so for that case better communicate with Chris/Jakob on how to proceed
  
  g) If step g has been successful, simply leave a comment if you think the description you added during step 7 (in the commit command) is not sufficient, and then push 
  `Create pull request`
  
  h) Not yet finalized! Someone has to review and merge into CMS-LUMI-POG's "master", before you see your nice work be released. Stay tuned and follow the discussion on the pull request page




