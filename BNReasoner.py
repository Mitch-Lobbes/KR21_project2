from typing import Union, Set
import copy
from networkx import DiGraph
from DSeparated import DSeparated
from BayesNet import BayesNet
from MAP import MAP
from MPE import MPE
from Ordering import Ordering
from typing import Set, Tuple
from NetworkPruner import FrenchPruning
from Marginal import Marginal
import pandas as pd


class BNReasoner:
    def __init__(self, net: Union[str, BayesNet]):
        """
        :param net: either file path of the bayesian network in BIFXML format or BayesNet object
        """
        if type(net) == str:
            # constructs a BN object
            self.bn = BayesNet()
            # Loads the BN from an BIFXML file
            self.bn.load_from_bifxml(net)
        else:
            self.bn = net

        self._d_sep = DSeparated()
        self._map = MAP(bn=self.bn)
        self.mpe = MPE()
        self._order = Ordering()
        self._pruning = FrenchPruning()
        self._marginal = Marginal(bn=self.bn)
            
    # UTILITY FUNCTIONS ------------------------------------------------------------------------------------------------
    # TODO: This is where your methods should go

    def d_separation(self, X: Set[str], Z: Set[str], Y: Set[str]) -> bool:
        return self._d_sep.d_separated(bayesNet=self.bn, X=X, Z=Z, Y=Y)

    def MAP(self, M: Set[str], E: dict[str, bool], order: list[str] = None) -> Tuple[float, dict[str, bool]]:
        p, assignments = self._map.MAP(M=M, E=E, order=order)
        return p, assignments

    def min_fill(self, X: list[str]) -> list[str]:
        return self._order.min_fill(bn=self.bn, X=X)

    def min_degree(self, X: list[str]) -> list[str]:
        return self._order.min_degree(bn=self.bn, X=X)

    def pruning(self, query: Set[str], evidence: dict[str, bool]) -> BayesNet:
        return self._pruning.run(bn=self.bn, query=query, evidence=evidence)

    def marginal(self, Q: Set[str], E: dict[str, bool], order: list = None) -> pd.DataFrame:
        return self._marginal.posterior_marginal(Q=Q, E=E, order=order)

    def MPE(self, evidence: dict[str, bool], order: list) -> pd.Series:
        return self.mpe.run(bn=self.bn, evidence=evidence, order=order)




