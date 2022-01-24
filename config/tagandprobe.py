from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List

import code_generation.producers.event as event
import code_generation.producers.muons as muons
import code_generation.producers.electrons as electrons
import code_generation.producers.pairquantities as pairquantities
import code_generation.producers.pairselection as pairselection
import code_generation.producers.embedding as emb
import code_generation.producers.triggers as triggers
import code_generation.producers.tagandprobe as tagandprobe
import code_generation.quantities.nanoAOD as nanoAOD
import code_generation.quantities.output as q
from code_generation.configuration import Configuration
from code_generation.rules import AppendProducer
from code_generation.modifiers import EraModifier, SampleModifier


def build_config(
    era: str,
    sample: str,
    channels: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_channels: List[str],
):

    if sample != "data" and sample != "emb" and sample != "dy":
        print("WARNING: TagandProbe measurement uses only data, dy and emb samples")
        exit()
    configuration = Configuration(
        era,
        sample,
        channels,
        shifts,
        available_sample_types,
        available_eras,
        available_channels,
    )
    # first add default parameters necessary for all scopes
    configuration.add_config_parameters(
        "global",
        {
            "min_muon_pt": 7.0,
            "max_muon_eta": 2.5,
            "max_muon_dxy": 1.0,
            "max_muon_dz": 1.0,
            "muon_iso_cut": 1.0,
            "min_ele_pt": 23.0,
            "max_ele_eta": 2.5,
            "max_ele_dxy": 0.045,
            "max_ele_dz": 0.2,
            "ele_id": nanoAOD.Electron_IDWP90,
            "max_ele_iso": 0.3,
        },
    )
    ###### Channel Specifics ######
    # MM channel Muon selection
    configuration.add_config_parameters(
        ["mm"],
        {
            "muon_index_in_pair": 0,
            "second_muon_index_in_pair": 1,
            "muon_iso_cut": 1.0,
            "min_muon_pt": 7.0,
            "max_muon_eta": 2.5,
            "max_muon_dxy": 1.0,
            "max_muon_dz": 1.0,
            "muon_id": "Muon_looseId",
            "pairselection_min_dR": 0.5,
        },
    )
    # MM Channel Trigger setup
    configuration.add_config_parameters(
        ["mm"],
        {
            "singlemoun_trigger": EraModifier(
                {
                    "2018": [
                        {
                            "flagname_1": "trg_IsoMu24_1",
                            "flagname_2": "trg_IsoMu24_2",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_IsoMu27_1",
                            "flagname_2": "trg_IsoMu27_2",
                            "hlt_path": "HLT_IsoMu27",
                            "ptcut": 28,
                            "etacut": 2.5,
                            "filterbit": 4,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_Mu17_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "ptcut": 18,
                            "etacut": 2.5,
                            "filterbit": 5,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZ_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZ_Mu8_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                            "ptcut": 8,
                            "etacut": 2.5,
                            "filterbit": 5,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZMass8_Mu17_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZMass8_Mu17_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "ptcut": 18,
                            "etacut": 2.5,
                            "filterbit": 5,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname_1": "trg_Mu17TrkMu8_DZMass8_Mu8_1",
                            "flagname_2": "trg_Mu17TrkMu8_DZMass8_Mu8_2",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
                            "ptcut": 8,
                            "etacut": 2.5,
                            "filterbit": 5,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
            #     "doublemuon_trigger": EraModifier(
            #         {
            #             "2018": [
            #                 {
            #                     "flagname_1": "trg_Mu17TrkMu8_DZ_1",
            #                     "flagname_2": "trg_Mu17TrkMu8_DZ_2",
            #                     "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
            #                     "p1_ptcut": 18,
            #                     "p2_ptcut": 9,
            #                     "p1_etacut": 2.5,
            #                     "p2_etacut": 2.5,
            #                     "p1_filterbit": 0,
            #                     "p1_trigger_particle_id": 13,
            #                     "p2_filterbit": 0,
            #                     "p2_trigger_particle_id": 13,
            #                     "max_deltaR_triggermatch": 0.4,
            #                 },
            #                 {
            #                     "flagname_1": "trg_Mu17TrkMu8_DZMass8_1",
            #                     "flagname_2": "trg_Mu17TrkMu8_DZMass8_2",
            #                     "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
            #                     "p1_ptcut": 18,
            #                     "p2_ptcut": 9,
            #                     "p1_etacut": 2.5,
            #                     "p2_etacut": 2.5,
            #                     "p1_filterbit": 0,
            #                     "p1_trigger_particle_id": 13,
            #                     "p2_filterbit": 0,
            #                     "p2_trigger_particle_id": 13,
            #                     "max_deltaR_triggermatch": 0.4,
            #                 },
            #             ],
            #         }
            #     ),
        },
    )

    # EE channel Electron selection
    configuration.add_config_parameters(
        ["ee"],
        {
            "electron_index_in_pair": 0,
            "second_electron_index_in_pair": 1,
            "min_electron_pt": 23.0,
            "max_electron_eta": 2.4,
            "max_electron_dxy": 0.045,
            "max_electron_dz": 0.2,
            "electron_id": nanoAOD.Electron_IDWP90,
        },
    )

    configuration.add_producers(
        "global",
        [
            # event.RunLumiEventFilter,
            event.Lumi,
            tagandprobe.BaseMuons,
            electrons.BaseElectrons,
        ],
    )
    configuration.add_producers(
        "mm",
        [
            muons.GoodMuons,
            muons.VetoMuons,
            muons.VetoSecondMuon,
            muons.ExtraMuonsVeto,
            muons.NumberOfGoodMuons,
            electrons.ExtraElectronsVeto,
            pairselection.MMPairSelection,
            pairselection.GoodMMPairFilter,
            pairselection.LVMu1,
            pairselection.LVMu2,
            pairselection.LVMu1Uncorrected,
            pairselection.LVMu2Uncorrected,
            pairquantities.MMDiTauPairQuantities,
            tagandprobe.MuonIDs,
            # triggers.MMGenerateSingleMuonTriggerFlags,
            tagandprobe.MMSingleMuonTriggerFlags_1,
            tagandprobe.MMSingleMuonTriggerFlags_2,
            # tagandprobe.MMDoubleMuonTriggerFlags_1,
            # tagandprobe.MMDoubleMuonTriggerFlags_2,
            # triggers.MMGenerateSingleMuonTriggerFlags_2,
        ],
    )

    # configuration.add_producers(
    #     "ee",
    #     [
    #         # electrons.GoodElectrons,
    #         electrons.VetoElectrons,
    #         # electrons.VetoSecondElectron,
    #         electrons.ExtraElectronsVeto,
    #         pairselection.EEPairSelection,
    #         pairselection.GoodEEPairFilter,
    #         pairselection.LVEl1,
    #         pairselection.LVEl2,
    #         pairquantities.EEDiTauPairQuantities,
    #     ],
    # )

    configuration.add_outputs(
        ["mm"],
        [
            nanoAOD.run,
            q.lumi,
            nanoAOD.event,
            q.pt_1,
            q.pt_2,
            q.eta_1,
            q.eta_2,
            q.phi_1,
            q.phi_2,
            q.id_medium_1,
            q.id_medium_2,
            q.id_loose_1,
            q.id_loose_2,
            q.id_tight_1,
            q.id_tight_2,
            q.m_vis,
            q.iso_1,
            q.iso_2,
            q.nmuons,
            q.is_global_1,
            q.is_global_2,
            q.muon_veto_flag,
            q.electron_veto_flag,
            tagandprobe.MMSingleMuonTriggerFlags_1.output_group,
            tagandprobe.MMSingleMuonTriggerFlags_2.output_group,
            # tagandprobe.MMDoubleMuonTriggerFlags_1.output_group,
            # tagandprobe.MMDoubleMuonTriggerFlags_2.output_group,
            # triggers.MMGenerateSingleMuonTriggerFlags_2.output_group,
        ],
    )

    configuration.add_outputs(
        ["ee"],
        [
            nanoAOD.run,
            q.lumi,
            nanoAOD.event,
            q.pt_1,
            q.pt_2,
            q.eta_1,
            q.eta_2,
            q.phi_1,
            q.phi_2,
            q.m_vis,
            q.iso_1,
            q.iso_2,
            q.electron_veto_flag,
        ],
    )

    configuration.add_modification_rule(
        "global",
        AppendProducer(producers=emb.EmbeddingQuantities, samples=["emb", "emb_mc"]),
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.dump_dict()
