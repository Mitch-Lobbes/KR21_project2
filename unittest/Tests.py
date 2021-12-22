import unittest
import copy
import numpy as np

from BNReasoner import BNReasoner
from DSeparated import DSeparated
from MAP import MAP
from MPE import MPE
from Marginal import Marginal
from NetworkPruner import NetworkPruner
from Ordering import Ordering


class Tests(unittest.TestCase):

    def setUp(self):
        network_one = "../testing/lecture_example.BIFXML"
        network_two = "../testing/lecture_example2.BIFXML"
        network_three = "../testing/dog_problem.BIFXML"
        
        self.reasoner_one = BNReasoner(net=network_one)
        self.marginal_one = Marginal(bn=self.reasoner_one.bn)
        self.map_one = MAP(bn=self.reasoner_one.bn)

        self.reasoner_two = BNReasoner(net=network_two)
        self.marginal_two = Marginal(bn=self.marginal_one.bn)
        self.map_two = MAP(bn=self.reasoner_two.bn)

        self.reasoner_three = BNReasoner(net=network_three)
        self.marginal_three = Marginal(bn=self.reasoner_three.bn)
        self.map_three = MAP(bn=self.reasoner_three.bn)

        self.d_seperated = DSeparated()
        self.ordering = Ordering()
        self.pruner = NetworkPruner()
        self.mpe = MPE()

    # -----------------------------------------------------------------------------------------------
    # D-Separation Tests ----------------------------------------------------------------------------
    def test_d_separation_actually_separated(self):
        X = {"bowel-problem"}
        Y = {"light-on"}
        Z = {"family-out"}
        self.reasoner_three.bn.draw_structure()
        result = self.d_seperated.d_separated(bayesNet=self.reasoner_three.bn, X=X, Y=Y, Z=Z)
        self.assertTrue(result)

    def test_d_separation_not_separated(self):
        X = {"bowel-problem"}
        Y = {"family-out"}
        Z = {"hear-bark"}
        self.reasoner_three.bn.draw_structure()
        result = self.d_seperated.d_separated(bayesNet=self.reasoner_three.bn, X=X, Y=Y, Z=Z)
        self.assertFalse(result)

    # -----------------------------------------------------------------------------------------------
    # Ordering Tests --------------------------------------------------------------------------------
    def test_min_degree_ordering(self):
        vars = self.reasoner_one.bn.get_all_variables()
        order = self.ordering.min_degree(bn=self.reasoner_one.bn, X=vars)
        self.assertListEqual(order, ['Slippery Road?', 'Winter?', 'Sprinkler?', 'Rain?', 'Wet Grass?'])

    def test_min_fill_ordering(self):
        vars = self.reasoner_one.bn.get_all_variables()
        order = self.ordering.min_fill(bn=self.reasoner_one.bn, X=vars)
        self.assertListEqual(order, ['Winter?', 'Sprinkler?', 'Wet Grass?', 'Rain?', 'Slippery Road?'])

    # -----------------------------------------------------------------------------------------------
    # Network Pruning Tests -------------------------------------------------------------------------
    def test_pruning_one(self):
        test_reasoner = copy.deepcopy(self.reasoner_two)
        query = {'X', 'Y'}
        evidence = {'J': True}
        self.pruner.run(bn=test_reasoner.bn, query=query,evidence=evidence)
        self.reasoner_two.bn.draw_structure()
        self.assertFalse('O' in test_reasoner.bn.get_all_variables())
        self.assertTrue(len(test_reasoner.bn.get_edges_ingoing_to_var('X')) == 1)
        self.assertTrue(test_reasoner.bn.get_edges_ingoing_to_var('X')[0][0] == 'I')
        self.assertTrue(len(test_reasoner.bn.get_edges_ingoing_to_var('Y')) == 0)

    def test_pruning_two(self):
        test_reasoner = copy.deepcopy(self.reasoner_two)
        test_reasoner.bn.draw_structure()
        query = {'I'}
        evidence = {'X': False}
        self.pruner.run(bn=test_reasoner.bn, query=query,evidence=evidence)
        test_reasoner.bn.draw_structure()
        self.assertFalse('O' in test_reasoner.bn.get_all_variables())
        self.assertTrue(len(test_reasoner.bn.get_edges()) == 3)

    # -----------------------------------------------------------------------------------------------
    # Marginal Distribution Test --------------------------------------------------------------------
    def test_marginal_dist(self):
        Q = {"Wet Grass?", "Slippery Road?"}
        E = {"Winter?": True, "Sprinkler?": False}
        result = self.marginal_one.posterior_marginal(Q=Q, E=E)
        self.assertListEqual(list(np.around(np.array(list(result['p'])), 3)),
                             [0.2480, 0.192, 0.112, 0.448])

    # -----------------------------------------------------------------------------------------------
    # MAP Test --------------------------------------------------------------------------------------
    def test_map(self):
        Q = {"I", "J"}
        E = {"O": True}
        result = self.map_two.MAP(M=Q, E=E)
        self.assertTrue(result[0] == 0.24272)
        self.assertFalse(result[1]['J'])
        # 'I' can be both True and False with equal prob, so just check if it exists
        self.assertTrue('I' in result[1])

    # -----------------------------------------------------------------------------------------------
    # MPE Test --------------------------------------------------------------------------------------
    def test_mpe(self):
        E = {"X": True}
        order = ['I', 'J', 'Y', 'O', 'X']
        result = self.mpe.run(bn=self.reasoner_two.bn, evidence=E, order=order)
        self.assertTrue(result['X'])
        self.assertTrue(result['p'] == 0.2304225)
