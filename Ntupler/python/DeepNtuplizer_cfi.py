import FWCore.ParameterSet.Config as cms

deepntuplizer = cms.EDAnalyzer('DeepNtuplizer',
                                pfcands    = cms.InputTag("packedPFCandidates"),
                                vertices   = cms.InputTag("offlineSlimmedPrimaryVertices"),
                                puInfo     = cms.InputTag("slimmedAddPileupInfo"),
                                rhoInfo    = cms.InputTag("fixedGridRhoFastjetAll"),
                                jets       = cms.InputTag("slimmedJets"),
                                jetR       = cms.double(0.4),
                                SVs        = cms.InputTag("slimmedSecondaryVertices"),
                                genJetsMatch = cms.InputTag('ak4GenJetsWithNuMatch'),
                                genParticles = cms.InputTag("prunedGenParticles"),
                                jetPtMin     = cms.untracked.double(15),
                                jetPtMax     = cms.untracked.double(1000),
                                jetAbsEtaMax = cms.untracked.double(99),
                                bDiscriminators = cms.vstring(),
                                isPuppiJets   = cms.bool(False),
                                isQCDSample   = cms.untracked.bool(False),
                                isPythia      = cms.bool(False),
                                isHerwig      = cms.bool(False),
                                isMadGraph    = cms.bool(False),
                                isTrainSample = cms.untracked.bool(True),
                                )
