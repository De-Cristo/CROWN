from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List

from .producers import event as event
from .producers import triggers as triggers
from .producers import genparticles as genparticles
from .producers import muons as muons
from .producers import jets as jets
from .producers import scalefactors as scalefactors
from .quantities import nanoAOD as nanoAOD
from .quantities import output as q
from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier
from code_generation.rules import RemoveProducer
from code_generation.systematics import SystematicShift


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
):

    configuration = Configuration(
        era,
        sample,
        scopes,
        shifts,
        available_sample_types,
        available_eras,
        available_scopes,
    )

    configuration.add_config_parameters(
        "global",
        {
            "PU_reweighting_file": EraModifier(
                {
                    "2016": "data/pileup/Data_Pileup_2016_271036-284044_13TeVMoriond17_23Sep2016ReReco_69p2mbMinBiasXS.root",
                    "2017": "data/pileup/Data_Pileup_2017_294927-306462_13TeVSummer17_PromptReco_69p2mbMinBiasXS.root",
                    "2018": "data/pileup/Data_Pileup_2018_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18.root",
                }
            ),
            "golden_json_file": EraModifier(
                {
                    "2016": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2017": "data/golden_json/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
                    "2018": "data/golden_json/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt",
                }
            ),
            "PU_reweighting_hist": "pileup",
            "met_filters": EraModifier(
                {
                    "2016": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        # "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                    ],
                    "2017": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        # "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                    "2018": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        # "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                }
            ),
        },
    )

    # vh add triggers (copying htautau mtau TODO)
    configuration.add_config_parameters(
        ["e2m","m2m", "2e2m","4m"],
        {
            "singlemuon_trigger": EraModifier(
                {
                # vh TODO update pT threshold in trigger matching
                    "2018": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu27",
                            "hlt_path": "HLT_IsoMu27",
                            "ptcut": 28,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu27",
                            "hlt_path": "HLT_IsoMu27",
                            "ptcut": 28,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016": [
                        {
                            "flagname": "trg_single_mu22",
                            "hlt_path": "HLT_IsoMu22",
                            "ptcut": 23,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
        },
    )

    # muon base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_muon_pt": 20.0, # vh
            "max_muon_eta": 2.4, # vh
            "max_muon_dxy": 0.05, # vh
            "max_muon_dz": 0.10, # vh
            "max_sip3d" : 8.0, # vh
            #"min_lepmva" : 0.4, # vh TODO
            "muon_id": "Muon_mediumId", # vh cut-based atm https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2#Medium_Muon
            "muon_iso_cut": 0.25, # vh PFIsoLoose dR=0.4 https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2#Particle_Flow_isolation
        },
    )
    # MM scope Muon selection
    configuration.add_config_parameters(
        ["m2m"],
        {
            "muon_index_in_pair": 0,
            "second_muon_index_in_pair": 1,
            "min_muon_pt": 23.0,
            "max_muon_eta": 2.1,
            "muon_iso_cut": 0.15,
        },
    )
    # Muon scale factors configuration
    configuration.add_config_parameters(
        ["m2m"],
        {
            "muon_sf_file": EraModifier(
                {
                    "2016": "data/jsonpog-integration/POG/MUO/2016postVFP_UL/muon_Z.json.gz",
                    "2017": "data/jsonpog-integration/POG/MUO/2017_UL/muon_Z.json.gz",
                    "2018": "data/jsonpog-integration/POG/MUO/2018_UL/muon_Z.json.gz",
                }
            ),
            "muon_id_sf_name": "NUM_MediumID_DEN_TrackerMuons",
            "muon_iso_sf_name": "NUM_TightRelIso_DEN_MediumID",
            "muon_sf_year_id": EraModifier(
                {
                    "2016": "2016postVFP_UL",
                    "2017": "2017_UL",
                    "2018": "2018_UL",
                }
            ),
            "muon_sf_varation": "sf",  # "sf" is nominal, "systup"/"systdown" are up/down variations
        },
    )

    # jet base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_jet_pt": 25, # vh
            "max_jet_eta": 4.7, # vh
            # vh TODO jet id
            "jet_id": 2,  # default: 2==pass tight ID and fail tightLepVeto
            # vh TODO jet puid
            "jet_puid": EraModifier(
                {
                    "2016preVFP": 1,  # 0==fail, 1==pass(loose), 3==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2016postVFP": 1,  # 0==fail, 1==pass(loose), 3==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2017": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2018": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                }
            ),
            "jet_puid_max_pt": 50,  # recommended to apply puID only for jets below 50 GeV
            "deltaR_jet_veto": 0.4, # vh jet-muon dR<0.4 overlap removal
            "jet_reapplyJES": False,
            "jet_jes_sources": '{""}',
            "jet_jes_shift": 0,
            "jet_jer_shift": '"nom"',  # or '"up"', '"down"'
            "jet_jec_file": EraModifier(
                {
                    "2016preVFP": '"data/jsonpog-integration/POG/JME/2016preVFP_UL/jet_jerc.json.gz"',
                    "2016postVFP": '"data/jsonpog-integration/POG/JME/2016postVFP_UL/jet_jerc.json.gz"',
                    "2017": '"data/jsonpog-integration/POG/JME/2017_UL/jet_jerc.json.gz"',
                    "2018": '"data/jsonpog-integration/POG/JME/2018_UL/jet_jerc.json.gz"',
                }
            ),
            "jet_jer_tag": EraModifier(
                {
                    "2016preVFP": '"Summer20UL16APV_JRV3_MC"',
                    "2016postVFP": '"Summer20UL16_JRV3_MC"',
                    "2017": '"Summer19UL17_JRV2_MC"',
                    "2018": '"Summer19UL18_JRV2_MC"',
                }
            ),
            "jet_jes_tag_data": '""',
            "jet_jes_tag": EraModifier(
                {
                    "2016preVFP": '"Summer19UL16APV_V7_MC"',
                    "2016postVFP": '"Summer19UL16_V7_MC"',
                    "2017": '"Summer19UL17_V5_MC"',
                    "2018": '"Summer19UL18_V5_MC"',
                }
            ),
            "jet_jec_algo": '"AK4PFchs"',
        },
    )
    # bjet base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_bjet_pt": 25, # vh
            "max_bjet_eta": EraModifier( # vh TODO
                {
                    "2016": 2.4,
                    "2017": 2.5,
                    "2018": 2.5,
                }
            ),
            "btag_cut_loose": EraModifier(  # loose # vh TODO update this for DeepCSV
                {
                    "2016": 0.3093,
                    "2017": 0.3040,
                    "2018": 0.2783,
                }
            ),
            "btag_cut_medium": EraModifier(  # medium # vh TODO verify this for DeepCSV
                {
                    "2016": 0.3093,
                    "2017": 0.3040,
                    "2018": 0.2783,
                }
            ),
        },
    )

    # veto ttH
    configuration.add_config_parameters(
        "global",
        {
            "vetottH_max_nbjets_loose" : 1,
            "vetottH_max_nbjets_medium" : 0,
        }
    )

    # m2m cuts
    configuration.add_config_parameters(
        "m2m",
        {
            "vh_m2m_nmuons" : 1,
        }
    )

    ## all scopes misc settings
    configuration.add_config_parameters(
        scopes,
        {
            "pairselection_min_dR": 0.5,
        },
    )

    configuration.add_producers(
        "global",
        [
            event.SampleFlags,
            event.PUweights,
            event.Lumi,
            event.MetFilter,
            muons.BaseMuons, # vh
            # vh muon Rochester corr, FSR recovery, GeoFit? TODO
            # vh muon FSR recovery
            #electrons.BaseElectrons, # vh TODO
            jets.JetEnergyCorrection, # vh
            jets.GoodJets, # vh overlap removal with ?base? muons done [need validation]
            jets.GoodBJetsLoose, # vh TODO update btag
            jets.GoodBJetsMedium, # vh TODO update btag
            jets.NumberOfLooseB, # vh count loose bjets for ttH veto
            jets.NumberOfMediumB, # vh count medium bjets for ttH veto
            event.VetottHLooseB, # vh veto ttH no more than 1 loose bjet
            event.VetottHMediumB, # vh veto ttH no more than 1 medium bjet
        ],
    )
    configuration.add_producers(
        "m2m",
        [
            muons.GoodMuons, # vh tighter selections on muons
            muons.NumberOfGoodMuons,
            event.FilterNMuons, # vh ==3 muons
            muons.MuonCollection, # vh
            muons.LVMu1, # vh
            muons.LVMu2, # vh
            muons.LVMu3, # vh
            #scalefactors.MuonIDIso_SF, # TODO 3 muon SF
            # vh veto e
            # vh total charge = +/-1
            # vh low mll veto, mll>12 GeV
            # vh m(mumu) in [110, 150] GeV, >=1 pair
            # vh select higher pT mumu pair as Higgs if there are >=1
            # vh no m(mumu) in [81, 101] GeV, 0 pair
            # vh
            triggers.GenerateSingleMuonTriggerFlags, # vh check trigger matching TODO
            # vh the trigger-matched muon should have pT > 29 (26) for 2017 (2016,18)
        ],
    )

    configuration.add_outputs(
        "m2m",
        [
            q.is_data,
            q.is_embedding,
            q.is_ttbar,
            q.is_dyjets,
            q.is_wjets,
            q.is_diboson,
            nanoAOD.run,
            q.lumi,
            nanoAOD.event,
            q.puweight,
            #q.pt_1,
            #q.pt_2,
            #q.eta_1,
            #q.eta_2,
            #q.phi_1,
            #q.phi_2,
            #q.m_vis,
            #q.gen_pt_1,
            #q.gen_eta_1,
            #q.gen_phi_1,
            #q.gen_mass_1,
            #q.gen_pdgid_1,
            #q.gen_pt_2,
            #q.gen_eta_2,
            #q.gen_phi_2,
            #q.gen_mass_2,
            #q.gen_pdgid_2,
            #q.gen_m_vis,
            #q.id_wgt_mu_1,
            #q.id_wgt_mu_2,
            #q.iso_wgt_mu_1,
            #q.iso_wgt_mu_2,
        ],
    )

    configuration.add_modification_rule(
        "global",
        RemoveProducer(
            producers=[event.PUweights],
            samples=["data"],
        ),
    )
    configuration.add_modification_rule(
        "m2m",
        RemoveProducer(
            producers=[
                genparticles.MMGenDiTauPairQuantities,
                scalefactors.MuonIDIso_SF,
            ],
            samples=["data"],
        ),
    )

    configuration.add_shift(
        SystematicShift(
            name="MuonIDUp",
            shift_config={"m2m": {"muon_sf_varation": "systup"}},
            producers={
                "m2m": [
                    scalefactors.Muon_1_ID_SF,
                    scalefactors.Muon_2_ID_SF,
                ]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="MuonIDDown",
            shift_config={"m2m": {"muon_sf_varation": "systdown"}},
            producers={
                "m2m": [
                    scalefactors.Muon_1_ID_SF,
                    scalefactors.Muon_2_ID_SF,
                ]
            },
        )
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
