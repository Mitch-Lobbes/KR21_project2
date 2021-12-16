import unittest

from BNReasoner import BNReasoner
from NetworkPruner import NetworkPruner


class NetworkPrunerTests(unittest.TestCase):

    def setUp(self):
        network = "../testing/lecture_example2.BIFXML"
        self.reasoner = BNReasoner(net=network)

    def test_node_pruning(self):
        pruner = NetworkPruner(bn=self.reasoner.bn)
        Q = set("X")
        E = set("J")
        res = pruner.prune(Q=Q, E=E)
        self.assertTrue(len(res.get_all_variables()) == 3)
        x = 5


if __name__ == '__main__':
    unittest.main()