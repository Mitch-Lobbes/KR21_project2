from BNReasoner import BNReasoner
import pandas as pd
from ordering import Ordering
from d_separation import DSeparated
import networkx as nx

NETWORK = "testing/dog_problem.BIFXML"
reasoner = BNReasoner(net=NETWORK)

orderer = Ordering()
X = ["light-on", "dog-out", "family-out"]

result = orderer.min_fill(
    bn = reasoner.bn,
    X = X
)

print(result)