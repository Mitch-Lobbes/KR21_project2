import unittest

from BNReasoner import BNReasoner
from Distribution import Distribution


class DistributionsTests(unittest.TestCase):

    def setUp(self):
        network = "../testing/lecture_example.BIFXML"
        self.reasoner = BNReasoner(net=network)
        self.distribution = Distribution(bn=self.reasoner.bn)

    def test_marginal_distribution(self):
        Q = {"Rain?"}
        E = {"Winter?": True}
        result = self.distribution.joint_marginal(Q=Q, E=E)
        x = 5
