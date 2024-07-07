# DNNTuples for AK4 jets

## Setup
```
# use CMSSW_13_2_11
cmsrel CMSSW_13_2_11
cd CMSSW_13_2_11/src
cmsenv

# Set up upon Andre's repo 

git cms-merge-topic stahlleiton:HiForest_TTbar 


# clone this repo into "DeepNTuples" directory
git clone git@github.com:dickychant/DNNTuples.git DeepNTuples -b dev/ak4/Run3HI/13_2_X

scram b -j8

cd DeepNTuples/Ntupler/test
cmsRun AK4PFJetsHI.py #
```

## Current limitation
1. First output of such: https://root.cern/js/latest/?file=https://sqian.web.cern.ch/sqian/first_HI_dnntupler.root 
2. SV infomation screwed up
3. B definition not working...
4. GenParticles not good?

## Submit jobs via CRAB

**Step 0**: switch to the crab production directory and set up grid proxy, CRAB environment, etc.

```bash
cd $CMSSW_BASE/src/DeepNTuples/Ntupler/run
# set up grid proxy
voms-proxy-init -rfc -voms cms --valid 168:00
# set up CRAB env (must be done after cmsenv)
source /cvmfs/cms.cern.ch/common/crab-setup.sh
```

**Step 1**: use the `crab.py` script to submit the CRAB jobs:

`python3 crab.py --set-input-dataset -p ../test/DeepNtuplizerAK4[CHS|Puppi].py --site T2_CH_CERN -o /store/user/$USER/DeepNtuples/[version] -t DeepNtuplesAK4-[version] --no-publication -i [ABC].conf -s FileBased -n 1 --work-area crab_projects_[ABC] --send-external [--input_files JEC.db] --dryrun`

These command will perform a "dryrun" to print out the CRAB configuration files. Please check everything is correct (e.g., the output path, version number, requested number of cores, etc.) before submitting the actual jobs. To actually submit the jobs to CRAB, just remove the `--dryrun` option at the end.

**[Note] For the QCD samples use `-n 1 --max-units 50` to run one file per job, and limit the total files per job to 50.**


**Step 2**: check job status

The status of the CRAB jobs can be checked with:

```bash
./crab.py --status --work-area crab_projects_[ABC]
```

Note that this will also resubmit failed jobs automatically.

The crab dashboard can also be used to get a quick overview of the job status:
`https://dashb-cms-job.cern.ch/dashboard/templates/task-analysis`

More options of this `crab.py` script can be found with:

```bash
./crab.py -h
```
