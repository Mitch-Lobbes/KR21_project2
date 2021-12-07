from BNReasoner import BNReasoner
from BayesNet import BayesNet
from d_separation import DSeparated
from network_pruning import FrenchPruning

NETWORK = "testing/lecture_example.BIFXML"


test = BayesNet()
test.load_from_bifxml(file_path=NETWORK)


#test.create_bn(variables = ["R", "E", "A", "C", "B"], edges = [("E", "R"), ("E", "A"), ("B", "A"), ("A", "C")], cpts = {'R': [1, 2], 'E': [3,4], 'A': [5,6], "C": [3,4], "B": [8,9]})
pruning = FrenchPruning()

pruning.run(bn=test, query={'Wet Grass?'}, evidence={'Winter?': True, 'Rain?': False})

test.draw_structure()

#reasoner = BNReasoner(test)
#
# d_seperator = DSeparated()
#
#
# X = set('R')
# Y = set('C')
# Z = set([])
#
# result = d_seperator.d_separated(
#     bayesNet=reasoner.bn,
#     X=X,
#     Z=Z,
#     Y=Y
# )
#
# print(result)
