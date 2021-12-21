import random
from BayesNet import BayesNet
from MPE import MPE
from Ordering import Ordering
from copy import deepcopy

# NETWORK = "/Users/mitchlobbes/Documents/Msc Artificial Intelligence/Period 1.2/KR/KR21_project2/testing/lecture_example.BIFXML"
# NETWORK = "/Users/mitchlobbes/Documents/Msc Artificial Intelligence/Period 1.2/KR/KR21_project2/testing/lecture_example2.BIFXML"
# NETWORK = "/Users/mitchlobbes/Documents/Msc Artificial Intelligence/Period 1.2/KR/KR21_project2/testing/dog_problem.BIFXML"
#NETWORK = "/Users/mitchlobbes/Documents/Msc Artificial Intelligence/Period 1.2/KR/KR21_project2/Networks/Small/asia.bif.BIFXML"
# NETWORK = "/Users/mitchlobbes/Documents/Msc Artificial Intelligence/Period 1.2/KR/KR21_project2/Networks/Small/cancer.bif.BIFXML"
# NETWORK = "/Users/mitchlobbes/Documents/Msc Artificial Intelligence/Period 1.2/KR/KR21_project2/Networks/Large/win95pts.bif.BIFXML"

# NETWORK = "/Users/mitchlobbes/Documents/Msc Artificial Intelligence/Period 1.2/KR/KR21_project2/Networks/VeryLarge/andes.bif.BIFXML"


test = BayesNet()
test.load_from_bifxml(file_path=NETWORK)
ordering = Ordering()
mpe = MPE()

vars = test.get_all_variables()
evidence_var = {random.choice(vars): True, random.choice(vars): True}
test2 = deepcopy(test)

#mpe.run(bn=test, evidence={'J': True, 'O': False})
#print(f"Evidence: {evidence_var}")
mpe.run(bn=test, evidence=evidence_var, order=0)
mpe.run(bn=test, evidence=evidence_var, order=1)








