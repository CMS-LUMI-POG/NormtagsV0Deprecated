export LD_LIBRARY_PATH=/afs/cern.ch/cms/lumi/brilconda-1.1.7/root/lib
export PYTHONPATH=/afs/cern.ch/cms/lumi/brilconda-1.1.7/root/lib
export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH
export ROOTSYS=/afs/cern.ch/cms/lumi/brilconda-1.1.7/root
export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH
pip uninstall brilws  -y
pip install --install-option="--prefix=$HOME/.local" brilws 
echo "Is your username listed in remote list?"
echo
git remote -v
echo
echo "If not, do 'git remote add YOURGITUSERNAME git@github.com:YOURGITUSERNAME/VdMFramework.git'."
