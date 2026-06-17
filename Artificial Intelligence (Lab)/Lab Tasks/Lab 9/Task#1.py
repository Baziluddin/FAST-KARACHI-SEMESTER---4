from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

model = DiscreteBayesianNetwork([
    ('Education','Interview'),
    ('Experience','Interview'),
    ('Interview','HiringDecision')
])

cpd_E = TabularCPD(variable='Education', variable_card=2, values=[[0.65],[0.35]])
cpd_X = TabularCPD(variable='Experience', variable_card=2, values=[[0.5],[0.5]])

cpd_I = TabularCPD(
    variable='Interview',
    variable_card=2,
    values=[
        [0.9,0.7,0.6,0.2],
        [0.1,0.3,0.4,0.8]
    ],
    evidence=['Education','Experience'],
    evidence_card=[2,2]
)

cpd_H = TabularCPD(
    variable='HiringDecision',
    variable_card=2,
    values=[
        [0.85,0.3],
        [0.15,0.7]
    ],
    evidence=['Interview'],
    evidence_card=[2]
)

model.add_cpds(cpd_E, cpd_X, cpd_I, cpd_H)

model.check_model()

infer = VariableElimination(model)
result = infer.query(variables=['HiringDecision'])

print(result)
