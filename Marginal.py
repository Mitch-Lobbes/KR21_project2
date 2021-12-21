from typing import Set, Tuple
import pandas as pd
from sklearn import preprocessing
import copy

from BNUtils import BNUtils
from BayesNet import BayesNet
from Ordering import Ordering


class Marginal:

    def __init__(self, bn: BayesNet):
        self.bn = bn

    def posterior_marginal(self, Q: Set[str], E: dict[str, bool], order: list = None) -> pd.DataFrame:
        """Compute the posterior marginal P(Q|E)

        :param Q: Set of query variables
        :param E: Dict of evidence of variables with their assignment
        :param order: Optional ordering set
        :return: DataFrame of the marginal distribution
        """
        if not order:
            order = Ordering().min_degree(
                bn=self.bn,
                X=list(set(self.bn.get_all_variables()) - Q)
            )
        S = self.bn.get_all_cpts()
        for var, cpt in S.items():
            S[var] = self._remove_evidence_row(cpt=cpt, E=E)
        counter = 0
        for variable in order:
            cpts_with_var = self._cpts_containing_var(S, variable=variable)
            cpt_list = list(cpts_with_var.values())
            f = cpt_list[0]
            for i in range(len(cpts_with_var) - 1):
                f = BNUtils.multiply_factors(f, cpt2=cpt_list[i + 1])
            f_i = BNUtils.sum_out_var(cpt=f, variable=variable)
            for var, cpt in cpts_with_var.items():
                del S[var]
            S[str(counter)] = f_i
            counter += 1
        S_list = list(S.values())
        result_cpt = S_list[0]
        for i in range(len(S_list) - 1):
            result_cpt = BNUtils.multiply_factors(result_cpt, cpt2=S_list[i + 1])

        evidence_prob = 1
        # If evidence is given, compute the prob
        if E:
            evidence_vars_cpt = self.posterior_marginal(
                Q=set(E.keys()),
                E=dict()
            )
            for var, assignment in E.items():
                evidence_vars_cpt = evidence_vars_cpt[evidence_vars_cpt[var] == assignment]
            evidence_prob = evidence_vars_cpt.iloc[0]['p']
        result_cpt['p'] /= evidence_prob
        return result_cpt


    def _cpts_containing_var(self, cpts: dict[str, pd.DataFrame], variable:str) -> dict[str, pd.DataFrame]:
        return {var: cpt for var, cpt in cpts.items() if variable in cpt.columns}

    def _remove_evidence_row(self, cpt: pd.DataFrame, E: dict[str, bool]) -> pd.DataFrame:
        for evidence_var, evidence_assignment in E.items():
            if evidence_var in cpt.columns:
                cpt.loc[cpt[evidence_var] != evidence_assignment, 'p'] = 0
        return cpt


