from BNReasoner import BNReasoner
from BayesNet import BayesNet
from d_separation import DSeparated

NETWORK = "testing/lecture_example2.BIFXML"


test = BayesNet()
test.create_bn(variables = ["R", "E", "A", "C", "B"], edges = [("E", "R"), ("E", "A"), ("B", "A"), ("A", "C")], cpts = {'R': [1, 2], 'E': [3,4], 'A': [5,6], "C": [3,4], "B": [8,9]})

reasoner = BNReasoner(test)

d_seperator = DSeparated()


X = set('R')
Y = set('C')
Z = set([])

result = d_seperator.d_separated(
    bayesNet=reasoner.bn,
    X=X,
    Z=Z,
    Y=Y
)

print(result)
