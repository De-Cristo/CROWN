from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import ExtendedVectorProducer

####################
# Set of producers used for trigger flags
####################

GenerateSingleMuonTriggerFlags = ExtendedVectorProducer(
    name="GenerateSingleMuonTriggerFlags",
    call='trigger::GenerateTripleTriggerORFlag({df}, {output}, {input}, "{hlt_path}", {ptcut}, {ptcut}, {ptcut}, {etacut}, {etacut}, {etacut}, {trigger_particle_id}, {trigger_particle_id}, {trigger_particle_id}, {filterbit}, {filterbit}, {filterbit}, {max_deltaR_triggermatch} )',
    input=[
        q.muon_p4_1,
        q.muon_p4_2,
        q.muon_p4_3,
        nanoAOD.TriggerObject_bit,
        nanoAOD.TriggerObject_id,
        nanoAOD.TriggerObject_pt,
        nanoAOD.TriggerObject_eta,
        nanoAOD.TriggerObject_phi,
    ],
    output="flagname",
    scope=["e2m","m2m", "2e2m","4m"],
    vec_config="singlemuon_trigger",
)
