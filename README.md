## Normtags

##Basic Git Instructions

0. Create your own fork of CMS-LUMI-POG/Normtags (upper right)  

1. Check out the group's version of the tools (easiest way to keep in sync)  
    `git clone https://github.com/CMS-LUMI-POG/Normtags`

2. Step 1 clones only the master BRANCH of the CMS-LUMI-POG/Normtags (from now on origin). To fetch all the BRANCHES of the origin, 
   `git fetch origin`
   You can see the list of all BRANCHes with
   `git branch -a`

3. It is recommnened at this stage to checkout a new local branch in which you start to develop/edit files. This is done with
   `git checkout -b LOCAL_BRANCHNAME origin/REMOTE_BRANCHNAME`
   The name of LOCAL_BRANCHNAME could be whatever. For the list of available remote (and local) branches, you can simply type `git branch -a`.

4. Now, if you want to further release the local changes, the following steps (5-9) have to be done. Make a remote to your fork 
   `git remote add YOURGITUSERNAME http://github.com/YOURGITUSERNAME/Normtags`

5. Make sure that your remote repositoty has been added
    `git remote -v'

6. Make the first push to YOUR remote repository (fork).  To do this, it is necessary at least one file to have been edited/added. Check in your edited/created file(s) and commit with a descriptive comment 
   ```
    git add file1 file2  
    git commit -am "file1 and file2 are changed because..." 
   ```	  
7. Now, it is time to push the LOCAL_BRANCHNAME to YOUR fork.
    `git push YOURGITUSERNAME LOCAL_BRANCHNAME`
    It is also possible to give to the remote repository a different name with
     `git push YOURGITUSERNAME LOCAL_BRANCHNAME:NEW_BRANCHNAME`
8. If step 8 fails, i.e. if git complains with 
  "error: The requested URL returned error: 403 Forbidden while accessing https://github.com/YOURGITUSERNAME/Normtags.git/info/refs
  fatal: HTTP request failed"

  then simply add in the .git/config file the line:
  ` pushurl = git@github.com:YOURGITUSERNAME/Normtags.git `
  in the part of [remote "YOURGITUSERNAME"].

9. Make a pull request (PR) with your changes. The easiest way is to do it interactively on your github web interface
  
  a) Go to YOUR Normtags repository, i.e. https://github.com/YOURGITUSERNAME/Normtags
  
  b) You will see the indication 'New pull request' within the green context; you can click on it
  
  c) In the new screen of 'Comparing changes' there would be four instances, i.e. (BASE FORK, BASE) and (HEAD FORK, COMPARE)
  
  d) Select as BASE FORK "CMS-LUMI-POG/Normtags" and BASE "master"
  
  e) Select as HEAD FORK "YOURGITUSERNAME/Normtags" and COMPARE the branch name that you want to create the pull request for, e.g. the branch that it was created during steps 5-9
  
  f) An automatic message will be created. There should be 'Able to merge. These branches can be automatically merged.' If not the changes that you are trying to push cannot be automatically adapted. Furhter work will be needed, so for that case better communicate with Chris/Jakob on how to proceed
  
  g) If step g has been successful, simply leave a comment if you think the description you added during step 7 (in the commit command) is not sufficient, and then push 
  `Create pull request`
  
  h) Not yet finalized! Someone has to review and merge into CMS-LUMI-POG's "master", before you see your nice work be released. Stay tuned and follow the discussion on the pull request page




##Instructions for producing normtags per lumi section

  a) Make sure you have lumiValidate.py in your working directory (for plots).
  
     cp  ~cmsbril/public/lumiValidate.py .

  b) Steps:
  
     i) python makePerLumiNTs.py -f FillNo
     
        - Calls lumiValidate.py -f FillNo
     
     ii) Provides lumi sections available for each detector
     
     iii) Asks user for detector option: hfocv1, bcm1fv1, pltzerov1
     
     iv) User is then asked to enter runNo, and bad LS range(s)
     
     v) python makeBrilNTs.py to generate normtagv1.json
     
  c) As an example, let's say you would like to inspect Fill 4452. This particular fill has 3 different runs: 258174, 258175, and 258177. For simplicity, let's assume that pltzerov1 has bad data for run 258174 lumi sections 1 to 5, run 258175 lumi sections 100 to 120 and run 258177 1500 to 2100. Similary, 258174 30 38, 258175 1 100, 258177 100 500 for hfocv1 and  258174 1 10, 258175 1 124, 258177 1 1000 for bcm1fv1.
  
     python makePerLumiNTs.py -f 4452
     
     pltzerov1
     
     258174 1 5
     
     258175 1 120
     
     258177 1500 2100
     
     exit(ctrl-D or ctrl-C return)
     

Now you enter bad LS ranges for other detectors in a similar fashion (steps b, i-iv).

     more goodLS*.json should look like the following:

     ::::::::::::::
     goodLS_bcm1fv1.json
     ::::::::::::::
     ["bcm1fv1",{"258174":[[11,38]]}],
     ["bcm1fv1",{"258177":[[2048,2132]]}],
     ["bcm1fv1",{"258177":[[1001,2047]]}]
     ::::::::::::::
     goodLS_hfocv1.json
     ::::::::::::::
     ["hfocv1",{"258175":[[101,124]]}],
     ["hfocv1",{"258174":[[1,29]]}],
     ["hfocv1",{"258177":[[1,99]]}],
     ["hfocv1",{"258177":[[501,2132]]}]
     ::::::::::::::
     goodLS_pltzerov1.json
     ::::::::::::::
     ["pltzerov1",{"258175":[[1,99]]}],
     ["pltzerov1",{"258175":[[121,124]]}],
     ["pltzerov1",{"258174":[[6,38]]}],
     ["pltzerov1",{"258177":[[1,1499]]}],
     ["pltzerov1",{"258177":[[2101,2132]]}]

goodLS_det_type.json files are basically per normtag files for each detector. Now, to generate normtag file as per detector preference(pltzero, bcm1f, hfoc in desc. order by default), you just have to say

    python makeBrilNTs.py

This generates normtagv1.json file which should look like

    ["hfocv1",{"258174":[[1,5]]}],
    ["pltzerov1",{"258174":[[6,38]]}],
    ["pltzerov1",{"258175":[[1,99]]}],
    ["hfocv1",{"258175":[[101,120]]}],
    ["pltzerov1",{"258175":[[121,124]]}],
    ["pltzerov1",{"258177":[[1,1499]]}],
    ["bcm1fv1",{"258177":[[1500,2047]]}],
    ["bcm1fv1",{"258177":[[2048,2100]]}],
    ["pltzerov1",{"258177":[[2101,2132]]}]
