from typing import Set
import pandas as pd

from BNUtils import BNUtils
from BayesNet import BayesNet


class Distribution:

    def __init__(self, bn: BayesNet):
        self.bn = bn

    def marginal_distribution(self, Q: Set[str], E: dict[str, bool]) -> pd.DataFrame:
        """ Given query variables Q and a possibly empty evidence E, compute the marginal distribution P(Q|E)

        :param Q: Query variables
        :param E: Evidence variables
        :return: Marginal distribution P(Q|E)
        """

        # Marginalize out all variable not in Q U E
        vars_to_marginalize_out = self._get_vars_to_marginalize_out(Q=Q, E=E)
        y_cpt_before = self.bn.get_cpt("Y")
        for var in vars_to_marginalize_out:
            self._marginalize_out(var=var)
        y_cpt_after = self.bn.get_cpt("Y")

        return 5

    def _get_vars_to_marginalize_out(self, Q: Set[str], E: dict[str, bool]) -> Set[str]:
        all_vars = set(self.bn.get_all_variables())
        return all_vars - (set(E.keys()) | Q)

    def _marginalize_out(self, var: str):
        for key, cpt in self.bn.get_all_cpts().items():
            cpt = BNUtils.sum_out_var(cpt=cpt, variable=var)
            self.bn.update_cpt(cpt=cpt, variable=var)

