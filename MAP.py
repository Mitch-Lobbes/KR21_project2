import copy
from typing import Set, Tuple
import pandas as pd

from BNUtils import BNUtils
from BayesNet import BayesNet
from Marginal import Marginal
from NetworkPruner import FrenchPruning


class MAP:

    def __init__(self, bn: BayesNet):
        self._bn = bn
        self.marginal = Marginal(bn=bn)
        self.pruner = FrenchPruning()
        self._evidence = {}

    def MAP(self, M: Set[str], E: dict[str, bool], order: list[str] = None) -> Tuple[float, dict[str, bool]]:
        assignments = dict()

        self._evidence = E

        # Prune
        self.pruner.run(
            bn=self._bn,
            query=M,
            evidence=E
        )
        if not order:
            order = list(set(self._bn.get_all_variables()) - M)
            order.extend(M)

        S = self._bn.get_all_cpts()
        for var, cpt in S.items():
            S[var] = self._remove_evidence_row(cpt=cpt, E=E)
        counter = 0
        for var in order:
            cpts_with_var = self._cpts_containing_var(S, variable=var)
            if not cpts_with_var:
                continue
            cpt_list = list(cpts_with_var.values())
            f = cpt_list[0]
            for i in range(len(cpts_with_var) - 1):
                f = BNUtils.multiply_factors(f, cpt2=cpt_list[i + 1])
            if var in M:
                f_i, assignment = self.super_max(cpt=f, variable=var)
                assignments.update(assignment)
            else:
                f_i = BNUtils.sum_out_var(cpt=f, variable=var)
            for var, cpt in cpts_with_var.items():
                del S[var]
            S[str(counter)] = f_i
            counter += 1
        S_list = list(S.values())
        result_cpt = S_list[0]
        for i in range(len(S_list) - 1):
            result_cpt = BNUtils.multiply_factors(result_cpt, cpt2=S_list[i + 1])
        return result_cpt['p'], assignments

    def _cpts_containing_var(self, cpts: dict[str, pd.DataFrame], variable: str) -> dict[str, pd.DataFrame]:
        cpts_containing_var = dict()
        for var, cpt in cpts.items():
            if type(cpt) is pd.Series or variable not in cpt.columns:
                continue
            cpts_containing_var[var] = cpt
        return cpts_containing_var

    def _remove_evidence_row(self, cpt: pd.DataFrame, E: dict[str, bool]) -> pd.DataFrame:
        for evidence_var, evidence_assignment in E.items():
            if evidence_var in cpt.columns:
                cpt.loc[cpt[evidence_var] != evidence_assignment, 'p'] = 0
        return cpt

    def _edge_pruning(self):
        all_edges = [self._bn.get_edges_outgoing_from_var(variable=var) for var in self._evidence]

        for edges_from_var in all_edges:
            self._bn.del_edges(edges=edges_from_var)

        for var, CPT in self._bn.get_all_cpts().items():
            NEW_CPT = self._bn.get_compatible_instantiations_table(instantiation=pd.Series(self._evidence), cpt=CPT)

            for ev_var in self._evidence.keys():
                if ev_var in NEW_CPT and ev_var != var:
                    NEW_CPT = NEW_CPT.drop(ev_var, axis=1)

            self._bn.update_cpt(variable=var, cpt=NEW_CPT)

    @staticmethod
    def super_max(cpt: pd.DataFrame, variable: str) -> (pd.DataFrame, dict[str, bool]):

        cols = [col for col in cpt.columns[:-1] if col != variable]

        if len(cols) != 0:
            cpt = cpt.sort_values(by=['p'])

            unique_vals2 = cpt.drop_duplicates(subset=cols, keep="last")

            assignment = list(unique_vals2[variable])[0]

            unique_vals2 = unique_vals2.drop(columns=variable)
            unique_vals2 = unique_vals2.reset_index(drop=True)

            return unique_vals2, {variable: assignment}

        cpt = cpt.loc[cpt['p'].idxmax()]
        assignment = cpt[variable]
        cpt = cpt.drop(variable)
        return cpt, {variable: assignment}
