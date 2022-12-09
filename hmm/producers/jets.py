from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

####################
# Set of producers used for selection possible good jets
####################

### energy corrections
# vh these pT corrections are copied from Htautau
# TODO check if L1FastJet L2L3 and residual corrections are consistent with hmm
JetPtCorrection = Producer(
    name="JetPtCorrection",
    call="physicsobject::jet::JetPtCorrection({df}, {output}, {input}, {jet_reapplyJES}, {jet_jes_sources}, {jet_jes_shift}, {jet_jer_shift}, {jet_jec_file}, {jet_jer_tag}, {jet_jes_tag}, {jet_jec_algo})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_area,
        nanoAOD.Jet_rawFactor,
        nanoAOD.Jet_ID,
        nanoAOD.GenJet_pt,
        nanoAOD.GenJet_eta,
        nanoAOD.GenJet_phi,
        nanoAOD.rho,
    ],
    output=[q.Jet_pt_corrected],
    scopes=["global"],
)
JetMassCorrection = Producer(
    name="JetMassCorrection",
    call="physicsobject::ObjectMassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_mass,
        nanoAOD.Jet_pt,
        q.Jet_pt_corrected,
    ],
    output=[q.Jet_mass_corrected],
    scopes=["global"],
)
JetEnergyCorrection = ProducerGroup(
    name="JetEnergyCorrection",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[JetPtCorrection, JetMassCorrection],
)

### selecting jets

JetPtCut = Producer(
    name="JetPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_jet_pt})",
    input=[q.Jet_pt_corrected],
    output=[],
    scopes=["global"],
)
BJetPtCut = Producer(
    name="BJetPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_bjet_pt})",
    input=[q.Jet_pt_corrected],
    output=[],
    scopes=["global"],
)
JetEtaCut = Producer(
    name="JetEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {max_jet_eta})",
    input=[nanoAOD.Jet_eta],
    output=[],
    scopes=["global"],
)
BJetEtaCut = Producer(
    name="BJetEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {max_bjet_eta})",
    input=[nanoAOD.Jet_eta],
    output=[],
    scopes=["global"],
)
JetIDCut = Producer(
    name="JetIDCut",
    call="physicsobject::jet::CutID({df}, {output}, {input}, {jet_id})",
    input=[nanoAOD.Jet_ID],
    output=[q.jet_id_mask],
    scopes=["global"],
)
JetPUIDCut = Producer(
    name="JetPUIDCut",
    call="physicsobject::jet::CutPUID({df}, {output}, {input}, {jet_puid}, {jet_puid_max_pt})",
    input=[nanoAOD.Jet_PUID, q.Jet_pt_corrected],
    output=[q.jet_puid_mask],
    scopes=["global"],
)
BTagCutLoose = Producer(
    name="BTagCutLoose",
    call="physicsobject::jet::CutRawID({df}, {input}, {output}, {btag_cut_loose})",
    input=[nanoAOD.BJet_discriminator],
    output=[],
    scopes=["global"],
)
BTagCutMedium = Producer(
    name="BTagCutMedium",
    call="physicsobject::jet::CutRawID({df}, {input}, {output}, {btag_cut_medium})",
    input=[nanoAOD.BJet_discriminator],
    output=[],
    scopes=["global"],
)

# vh veto overlapping jets against muons
# TODO this runs over all jets, not efficient!!!
# need to run over only good jets
VetoOverlappingJetsWithMuons = Producer(
    name="VetoOverlappingJetsWithMuons",
    call="jet::VetoOverlappingJets({df}, {output}, {input}, {deltaR_jet_veto})",
    input=[nanoAOD.Jet_eta, nanoAOD.Jet_phi, nanoAOD.Muon_eta, nanoAOD.Muon_phi, q.base_muons_mask], # vh base or good muon?
    output=[q.jet_overlap_veto_mask],
    scopes=["global"],
)

GoodJets = ProducerGroup(
    name="GoodJets",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.good_jets_mask],
    scopes=["global"],
    subproducers=[JetPtCut, JetEtaCut, JetIDCut, JetPUIDCut, VetoOverlappingJetsWithMuons],
)

GoodBJetsLoose = ProducerGroup(
    name="GoodBJetsLoose",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[q.good_jets_mask],
    output=[q.good_bjets_mask_loose],
    scopes=["global"],
    subproducers=[BJetPtCut, BJetEtaCut, BTagCutLoose],
)
GoodBJetsMedium = ProducerGroup(
    name="GoodBJetsMedium",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[q.good_bjets_mask_loose],
    output=[q.good_bjets_mask_medium],
    scopes=["global"],
    subproducers=[BTagCutMedium],
)

NumberOfLooseB = Producer(
    name="NumberOfLooseB",
    call="quantities::NumberOfGoodObjects({df}, {output}, {input})",
    input=[q.good_bjets_mask_loose],
    output=[q.nbjets_loose],
    scopes=["global"],
)
NumberOfMediumB = Producer(
    name="NumberOfMediumB",
    call="quantities::NumberOfGoodObjects({df}, {output}, {input})",
    input=[q.good_bjets_mask_medium],
    output=[q.nbjets_medium],
    scopes=["global"],
)

