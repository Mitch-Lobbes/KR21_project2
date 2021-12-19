from BNReasoner import BNReasoner
from BayesNet import BayesNet
from MAP import MAP

NETWORK = "testing/lecture_example2.BIFXML"
reasoner = BNReasoner(NETWORK)
map = MAP()

map.sum_out(
    bn=reasoner.bn,
    node="R"
)
