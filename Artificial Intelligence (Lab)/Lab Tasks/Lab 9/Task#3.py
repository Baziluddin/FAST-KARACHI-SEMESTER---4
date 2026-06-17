from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

model = DiscreteBayesianNetwork([
    ('AdExposure','WebsiteExperience'),
    ('WebsiteExperience','Purchase'),
    ('ProductPrice','Purchase')
])

cpd_A = TabularCPD('AdExposure', 2, [[0.6],[0.4]])

cpd_W = TabularCPD('WebsiteExperience', 2,
                   [[0.8,0.4],
                    [0.2,0.6]],
                   evidence=['AdExposure'],
                   evidence_card=[2])

cpd_P = TabularCPD('ProductPrice', 2, [[0.45],[0.55]])

cpd_C = TabularCPD('Purchase', 2,
                   [[0.9,0.6,0.7,0.2],
                    [0.1,0.4,0.3,0.8]],
                   evidence=['WebsiteExperience','ProductPrice'],
                   evidence_card=[2,2])

model.add_cpds(cpd_A, cpd_W, cpd_P, cpd_C)

print(model.check_model())

infer = VariableElimination(model)

q = infer.query(variables=['Purchase'], evidence={'AdExposure':0})
print(q)
