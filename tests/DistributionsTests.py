import unittest

from BNReasoner import BNReasoner
from Marginal import Marginal


class DistributionsTests(unittest.TestCase):

    def setUp(self):
        network = "../testing/lecture_example.BIFXML"
        self.reasoner = BNReasoner(net=network)
        self.distribution = Marginal(bn=self.reasoner.bn)

    def test_marginal_distribution(self):
        Q = {"Wet Grass?", "Slippery Road?"}
        E = {"Winter?": True, "Sprinkler?": False}
        result = self.distribution.posterior_marginal(Q=Q, E=E)
        x = 5
