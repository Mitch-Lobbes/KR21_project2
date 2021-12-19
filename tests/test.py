import random
from BayesNet import BayesNet
from MPE import MPE
from Ordering import Ordering


NETWORK = "testing/lecture_example2.BIFXML"


test1, test2, test3 = BayesNet(), BayesNet(), BayesNet()

test1.load_from_bifxml(file_path=NETWORK)
test2.load_from_bifxml(file_path=NETWORK)
test3.load_from_bifxml(file_path=NETWORK)

ordering = Ordering()

query1 = test1.get_all_variables()
query2 = test2.get_all_variables()
query3 = test3.get_all_variables()
random.shuffle(query3)

orderings = [(test1, ordering.min_degree(bn=test1, X=query1)),
             (test2, ordering.min_fill(bn=test2, X=query2)),
             (test3, query3)]
mpe = MPE()

for tup in orderings:
    mpe.run(tup[0], evidence={'J': True, 'O': False}, order=tup[1])


