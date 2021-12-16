from typing import Set, Tuple
import pandas as pd

from BNUtils import BNUtils
from BayesNet import BayesNet
from ordering import Ordering


class Distribution:

    def __init__(self, bn: BayesNet):
        self.bn = bn

    def joint_marginal(self, Q: Set[str], E: dict[str, bool]) -> pd.DataFrame:
        order = Ordering().min_degree(
            bn=self.bn,
            X=list(set(self.bn.get_all_variables()) - Q)
        )
        S = self.bn.get_all_cpts()
        S_list = list(S.values())
        for var, cpt in S.items():
            self._remove_evidence_row(cpt=cpt, E=E)

        for variable in order:
            cpts_with_var = self._cpts_containing_var(cpts=S_list, variable=variable)
            f = cpts_with_var[0]
            for i in range(len(cpts_with_var) - 1):
                f = self._multiply_factors(f, cpt2=cpts_with_var[i + 1])
            f_i = self._sum_out_var(cpt=f, variable=variable)

        result_cpt = S_list[0]
        for i in range(len(S_list) - 1):
            result_cpt = self._multiply_factors(result_cpt, cpt2=S_list[i + 1])
        return result_cpt


    def _cpts_containing_var(self, cpts: list[pd.DataFrame], variable:str) -> list[pd.DataFrame]:
        return [cpt for cpt in cpts if variable in cpt.columns]

    def _remove_evidence_row(self, cpt: pd.DataFrame, E: dict[str, bool]) -> pd.DataFrame:
        for evidence_var, evidence_assignment in E.items():
            if evidence_var in cpt.columns:
                cpt = cpt[cpt[evidence_var] == evidence_assignment]
        return cpt

    def marginal_distribution(self, Q: Set[str], E: dict[str, bool]) -> pd.DataFrame:
        """ Given query variables Q and a possibly empty evidence E, compute the marginal distribution P(Q|E)

        :param Q: Query variables
        :param E: Evidence variables
        :return: Marginal distribution P(Q|E)
        """

        return 5

    def _multiply_out_var(self, cpt: pd.DataFrame, evidence_variable: Tuple[str, bool], variable_prop: float) -> pd.DataFrame:
        # Remove all rows where the evidence value is wrong
        cpt = cpt[cpt[evidence_variable[0]] == evidence_variable[1]]
        # Delete column with evidence var
        cpt = cpt.drop(evidence_variable[0], 1)
        # Multiply p values with given value
        cpt['p'] *= variable_prop
        return cpt

    def _get_vars_to_marginalize_out(self, Q: Set[str], E: dict[str, bool]) -> Set[str]:
        all_vars = set(self.bn.get_all_variables())
        return all_vars - (set(E.keys()) | Q)

    def _marginalize_out(self, var: str):
        for key, cpt in self.bn.get_all_cpts().items():
            cpt = BNUtils.sum_out_var(cpt=cpt, variable=var)
            self.bn.update_cpt(cpt=cpt, variable=var)

    def _sum_out_var(self, cpt: pd.DataFrame, variable: str) -> pd.DataFrame:
        """Sum out a variable from a conditional probability table (CPT)

        Args:
            cpt (pd.DataFrame): Pandas DataFrame representation of the cpt
            variable (str): Variable to sum out

        Returns:
            pd.DataFrame: cpt after summing out the variable
        """
        mask = cpt[variable] == True
        var_true_df = cpt[mask].drop(variable, axis=1)
        var_false_df = cpt[~mask].drop(variable, axis=1)

        columns = [col for col in var_true_df.columns if col != 'p']

        resulting_df = pd.concat([var_true_df, var_false_df]).groupby(columns, as_index=False)["p"].sum()
        return resulting_df

    def _multiply_factors(self, cpt1: pd.DataFrame, cpt2: pd.DataFrame) -> pd.DataFrame:
        """Multiply two given factors

        Args:
            cpt1 (pd.DataFrame): Pandas DataFrame representation of first cpt
            cpt1 (pd.DataFrame): Pandas DataFrame representation of second cpt

        Returns:
            pd.DataFrame: cpt after multiplying cpt1 and cpt2
        """
        common_vars = list(
            set([col for col in f1.columns if col != 'p']) & set([col for col in f2.columns if col != 'p']))

        merged_df = pd.merge(cpt1, cpt2, on=common_vars)
        merged_df['p'] = (merged_df['p_x'] * merged_df['p_y'])
        merged_df.drop(['p_x', 'p_y'], inplace=True, axis=1)

        return merged_df
