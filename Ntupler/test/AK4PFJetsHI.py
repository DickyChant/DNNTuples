import FWCore.ParameterSet.Config as cms

# ---------------------------------------------------------
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')

options.outputFile = 'output.root'
options.inputFiles = 'file:/eos/cms/store/cmst3/group/hintt/Run3/MC/PbPb2023/Embedded/2024_04_19/POWHEG_5p36TeV_2023Run3/TT_hvq_POWHEG_Hydjet_5p36TeV_TuneCP5_2023Run3_MINIAOD_2024_04_19/240419_231333/0000/POWHEG_TT_hvq_MINIAOD_2.root'
# options.inputFiles = '/store/mc/RunIISummer19UL17MiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/MINIAODSIM/106X_mc2017_realistic_v6_ext2-v2/60000/E0502E95-AA7E-B441-9277-498113BA458C.root'
# options.inputFiles = '/store/mc/RunIISummer19UL17MiniAOD/TTToSemiLeptonic_mtop171p5_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/60000/F06BD23E-48AB-1F4D-A0FB-80DD370F4868.root'
options.maxEvents = -1

options.register('skipEvents', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "skip N events")
options.register('inputDataset',
                 '',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Input dataset")
options.register('isTrainSample', True, VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool, "if the sample is used for training")

options.parseArguments()

# globalTagMap = {
#     'auto': 'auto:run3_mc_HIon',
# }
#
# era = 'auto'
# for k in globalTagMap:
#     if k in options.inputDataset:
#         era = k
#
from Configuration.Eras.Era_Run3_pp_on_PbPb_2023_cff import Run3_pp_on_PbPb_2023
process = cms.Process('DNNFiller', Run3_pp_on_PbPb_2023)

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.options = cms.untracked.PSet(
    allowUnscheduled=cms.untracked.bool(True),
    wantSummary=cms.untracked.bool(False)
)

print('Using output file ' + options.outputFile)

process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string(options.outputFile))

process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(options.maxEvents))

process.source = cms.Source('PoolSource',
                            fileNames=cms.untracked.vstring(options.inputFiles),
                            skipEvents=cms.untracked.uint32(options.skipEvents)
                            )
# ---------------------------------------------------------
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2023_realistic_hi', '')
process.TransientTrackBuilderESProducer = cms.ESProducer("TransientTrackBuilderESProducer",
                                                         ComponentName=cms.string('TransientTrackBuilder')
                                                         )

process.hiSignalGenParticles = cms.EDProducer('HiSignalParticleProducer',
                                    src    = cms.InputTag('genParticles')
                                    )

process.load('HeavyIonsAnalysis.JetAnalysis.akCs4PFJetSequence_pponPbPb_mc_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.hiFJRhoAnalyzer_cff')

# Select the types of jets filled
addR3Jets = False
addR3FlowJets = False
addR4Jets = True
addR4FlowJets = False
matchJets = True             # Enables q/g and heavy flavor jet identification in MC

# Choose which additional information is added to jet trees
doHIJetID = True             # Fill jet ID and composition information branches
doWTARecluster = False        # Add jet phi and eta for WTA axis

# this is only for non-reclustered jets
addCandidateTagging = True


if addR3Jets or addR3FlowJets or addR4Jets or addR4FlowJets :
    process.load("HeavyIonsAnalysis.JetAnalysis.extraJets_cff")
    from HeavyIonsAnalysis.JetAnalysis.clusterJetsFromMiniAOD_cff import setupHeavyIonJets
    process.load("HeavyIonsAnalysis.JetAnalysis.candidateBtaggingMiniAOD_cff")

    if addR3Jets :
        process.jetsR3 = cms.Sequence()
        setupHeavyIonJets('akCs3PF', process.jetsR3, process, isMC = 1, radius = 0.30, JECTag = 'AK3PF', doFlow = False, matchJets = matchJets)
        process.akCs3PFpatJetCorrFactors.levels = ['L2Relative', 'L3Absolute']
        process.akCs3PFJetAnalyzer = process.akCs4PFJetAnalyzer.clone(jetTag = "akCs3PFpatJets", jetName = 'akCs3PF', genjetTag = "ak3GenJetsNoNu", matchJets = matchJets, matchTag = "ak3PFMatchingForakCs3PFpatJets", doHiJetID = doHIJetID, doWTARecluster = doWTARecluster)
        process.forest += process.extraJetsMC * process.jetsR3 * process.akCs3PFJetAnalyzer

    if addR3FlowJets :
        process.jetsR3flow = cms.Sequence()
        setupHeavyIonJets('akCs3PFFlow', process.jetsR3flow, process, isMC = 1, radius = 0.30, JECTag = 'AK3PF', doFlow = True, matchJets = matchJets)
        process.akCs3PFFlowpatJetCorrFactors.levels = ['L2Relative', 'L3Absolute']
        process.akFlowPuCs3PFJetAnalyzer = process.akCs4PFJetAnalyzer.clone(jetTag = "akCs3PFFlowpatJets", jetName = 'akCs3PFFlow', genjetTag = "ak3GenJetsNoNu", matchJets = matchJets, matchTag = "ak3PFMatchingForakCs3PFFlowpatJets", doHiJetID = doHIJetID, doWTARecluster = doWTARecluster)
        process.forest += process.extraFlowJetsMC * process.jetsR3flow * process.akFlowPuCs3PFJetAnalyzer

    if addR4Jets :
        # Recluster using an alias "0" in order not to get mixed up with the default AK4 collections
        process.jetsR4 = cms.Sequence()
        setupHeavyIonJets('akCs0PF', process.jetsR4, process, isMC = 1, radius = 0.40, JECTag = 'AK4PF', doFlow = False, matchJets = matchJets)
        process.ak4PFMatchingForakCs0PFJets.jetPtMin = process.akCs0PFJets.jetPtMin
        process.akCs0PFpatJetCorrFactors.levels = ['L2Relative', 'L3Absolute']
        process.akCs4PFJetAnalyzer.jetTag = 'akCs0PFpatJets'
        process.akCs4PFJetAnalyzer.jetName = 'akCs0PF'
        process.akCs4PFJetAnalyzer.matchJets = matchJets
        process.akCs4PFJetAnalyzer.matchTag = 'ak4PFMatchingForakCs0PFpatJets'
        process.akCs4PFJetAnalyzer.doHiJetID = doHIJetID
        process.akCs4PFJetAnalyzer.doWTARecluster = doWTARecluster
        process.ak4PFMatchedForakCs0PFpatJets = cms.EDProducer("JetMatcherDR", source = cms.InputTag("akCs0PFpatJets"), matched = cms.InputTag("ak4PFMatchingForakCs0PFpatJets"))
        # process.forest += process.extraJetsMC * process.jetsR4 * process.ak4PFMatchedForakCs0PFpatJets
        
        process.akCs0PFpatJets.embedPFCandidates = True

    if addR4FlowJets :
        process.jetsR4flow = cms.Sequence()
        setupHeavyIonJets('akCs4PFFlow', process.jetsR4flow, process, isMC = 1, radius = 0.40, JECTag = 'AK4PF', doFlow = True, matchJets = matchJets)
        process.akCs4PFFlowpatJetCorrFactors.levels = ['L2Relative', 'L3Absolute']
        process.akFlowPuCs4PFJetAnalyzer.jetTag = 'akCs4PFFlowpatJets'
        process.akFlowPuCs4PFJetAnalyzer.jetName = 'akCs4PFFlow'
        process.akFlowPuCs4PFJetAnalyzer.matchJets = matchJets
        process.akFlowPuCs4PFJetAnalyzer.matchTag = 'ak4PFMatchingForakCs4PFFlowpatJets'
        process.akFlowPuCs4PFJetAnalyzer.doHiJetID = doHIJetID
        process.akFlowPuCs4PFJetAnalyzer.doWTARecluster = doWTARecluster
        process.forest += process.extraFlowJetsMC * process.jetsR4flow * process.akFlowPuCs4PFJetAnalyzer 


if addCandidateTagging:
    process.load("HeavyIonsAnalysis.JetAnalysis.candidateBtaggingMiniAOD_cff")

    from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
    updateJetCollection(
        process,
        jetSource = cms.InputTag('akCs0PFpatJets'),
        jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
        btagDiscriminators = ['pfCombinedSecondaryVertexV2BJetTags', 'pfDeepCSVDiscriminatorsJetTags:BvsAll', 'pfDeepCSVDiscriminatorsJetTags:CvsB', 'pfDeepCSVDiscriminatorsJetTags:CvsL'], ## to add discriminators,
        btagPrefix = 'TEST',
    )

    process.updatedPatJets.addJetCorrFactors = False
    process.updatedPatJets.discriminatorSources = cms.VInputTag(
        cms.InputTag("pfDeepFlavourJetTagsSlimmedDeepFlavour","probb"),cms.InputTag("pfDeepFlavourJetTagsSlimmedDeepFlavour","probbb"), cms.InputTag("pfDeepFlavourJetTagsSlimmedDeepFlavour","probc"), cms.InputTag("pfDeepFlavourJetTagsSlimmedDeepFlavour","probg"), cms.InputTag("pfDeepFlavourJetTagsSlimmedDeepFlavour","problepb"),
        cms.InputTag("pfDeepFlavourJetTagsSlimmedDeepFlavour","probuds"),
        cms.InputTag("pfParticleTransformerAK4JetTagsSlimmedDeepFlavour","probb"), cms.InputTag("pfParticleTransformerAK4JetTagsSlimmedDeepFlavour","probbb"), cms.InputTag("pfParticleTransformerAK4JetTagsSlimmedDeepFlavour","probc"),
        cms.InputTag("pfParticleTransformerAK4JetTagsSlimmedDeepFlavour","probg"), cms.InputTag("pfParticleTransformerAK4JetTagsSlimmedDeepFlavour","problepb"), cms.InputTag("pfParticleTransformerAK4JetTagsSlimmedDeepFlavour","probuds"),
    )

    process.akCs4PFJetAnalyzer.jetTag = "updatedPatJets"
    process.akCs4PFJetAnalyzer.useNewBtaggers = True

    # process.forest += process.candidateBtagging * process.updatedPatJets * process.akCs4PFJetAnalyzer




srcJets = cms.InputTag("updatedPatJets")


from RecoBTag.ONNXRuntime.pfParticleNetAK4_cff import _pfParticleNetAK4JetTagsAll
bTagDiscriminators = [
    'pfDeepFlavourJetTags:probb',
    'pfDeepFlavourJetTags:probbb',
    'pfDeepFlavourJetTags:problepb',
    'pfDeepFlavourJetTags:probc',
    'pfDeepFlavourJetTags:probuds',
    'pfDeepFlavourJetTags:probg',
] + _pfParticleNetAK4JetTagsAll


#from PhysicsTools.PatAlgos.tools.helpers import getPatAlgosToolsTask
#patTask = getPatAlgosToolsTask(process)

from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
process.ak4GenJetsWithNu = ak4GenJets.clone(
    src='packedGenParticles'
)
jetR = 0.4
isPuppiJets = False
process.ak4GenJetsWithNuMatch = cms.EDProducer("GenJetMatcher",  # cut on deltaR; pick best by deltaR
                                               src=srcJets,  # RECO jets (any View<Jet> is ok)
                                               # GEN jets  (must be GenJetCollection)
                                               matched=cms.InputTag("ak4GenJetsWithNu"),
                                               mcPdgId=cms.vint32(),  # n/a
                                               mcStatus=cms.vint32(),  # n/a
                                               checkCharge=cms.bool(False),  # n/a
                                               maxDeltaR=cms.double(jetR),  # Minimum deltaR for the match
                                               # maxDPtRel   = cms.double(3.0),                  # Minimum deltaPt/Pt for the match (not used in GenJetMatcher)
                                               # Forbid two RECO objects to match to the same GEN object
                                               resolveAmbiguities=cms.bool(True),
                                               # False = just match input in order; True = pick lowest deltaR pair first
                                               resolveByMatchQuality=cms.bool(False),
                                               )
process.genJetTask = cms.Task(
    process.ak4GenJetsWithNu,
    process.ak4GenJetsWithNuMatch,
)

# DeepNtuplizer
process.load("DeepNTuples.Ntupler.DeepNtuplizer_cfi")
process.deepntuplizer.jets = srcJets
process.deepntuplizer.isPuppiJets = isPuppiJets
process.deepntuplizer.bDiscriminators = bTagDiscriminators

process.deepntuplizer.genJetsMatch = 'ak4GenJetsWithNuMatch'

process.deepntuplizer.isQCDSample = '/QCD_' in options.inputDataset
process.deepntuplizer.isPythia = 'pythia' in options.inputDataset.lower()
process.deepntuplizer.isHerwig = 'herwig' in options.inputDataset.lower()
# note: MG can be interfaced w/ either pythia or herwig
process.deepntuplizer.isMadGraph = 'madgraph' in options.inputDataset.lower()

process.deepntuplizer.isTrainSample = options.isTrainSample
if not options.inputDataset:
    # interactive running
    process.deepntuplizer.isTrainSample = False
#==============================================================================================================================#
process.p = cms.Path(
    process.hiSignalGenParticles + process.extraJetsMC * process.jetsR4 +  process.ak4PFMatchedForakCs0PFpatJets +process.candidateBtagging+ process.updatedPatJets + process.deepntuplizer
    )
#process.p.associate(patTask)
process.p.associate(process.genJetTask)
# process.p.associate(process.qgTask)
