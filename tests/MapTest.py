import unittest

from BNReasoner import BNReasoner
from MAP import MAP


class MapTest(unittest.TestCase):

    def setUp(self):
        network = "../testing/lecture_example2.BIFXML"
        self.reasoner = BNReasoner(net=network)
        self.map = MAP(bn=self.reasoner.bn)

    def test_node_pruning(self):
        Q = {"I", "J"}
        E = {"O": True}
        #E = dict()
        res = self.map.MAP(M=Q, E=E)
        x = 5


if __name__ == '__main__':
    unittest.main()