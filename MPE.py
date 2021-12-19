import itertools
from Ordering import Ordering
from BayesNet import BayesNet
from typing import Set
import pandas as pd
import numpy as np
from functools import reduce

class MPE:

    def __init__(self):
        self._bn: BayesNet
        self._evidence: dict[str, bool]
        self._ordering = Ordering()
        self._value_dict = {}

    def run(self, bn: BayesNet, evidence: dict[str, bool], order: list[str]):
        self._bn = bn
        self._evidence = evidence

        self._edge_pruning()

        #query = self._bn.get_all_variables()
        #ordered_query = self._ordering.min_fill(bn=self._bn, X=query)
        cpt_list = list(self._bn.get_all_cpts().values())

        for variable in order:
            factors = self._all_cpt_containing_var(cpt_list=cpt_list, variable=variable)
            headers = [list(cpt.columns) for cpt in factors]
            product = self._multiply(factors=factors)
            new_cpt = self._super_max(cpt=product, variable=variable)

            cpt_list = [cpt for cpt in cpt_list if list(cpt.columns) not in headers]

            cpt_list.append(new_cpt)

        trivial = pd.DataFrame({'p': [1.0], 'MPE': [self._value_dict]})
        trivial['p'] = [cpt_list[i].iloc[0]['p']*cpt_list[i+1].iloc[0]['p'] for i in range(len(cpt_list)-1)]
        print(f'\nThis is the MPE given the evidence {self._evidence}: \n {trivial}')
        return trivial

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
    def _all_cpt_containing_var(cpt_list: list[pd.DataFrame], variable: str) -> list[pd.DataFrame]:
        return [cpt for cpt in cpt_list if variable in cpt.columns]

    @staticmethod
    def _multiply(factors: list[pd.DataFrame]) -> pd.DataFrame:
        common_vars = reduce(np.intersect1d, ([factor.columns for factor in factors]))
        common_vars = list(np.delete(common_vars, np.where(common_vars == 'p')))

        merged_df = factors[0]

        for factor in factors[1:]:
            merged_df = pd.merge(merged_df, factor, on=common_vars)
            merged_df['p'] = (merged_df['p_x'] * merged_df['p_y'])
            merged_df.drop(['p_x', 'p_y'], inplace=True, axis=1)


        merged_df['p'] = merged_df['p'].astype(float)


        return merged_df

    def _super_max(self, cpt: pd.DataFrame, variable: str):

        values = cpt[variable].unique()
        indices = [cpt.loc[cpt[variable] == value]['p'].idxmax() for value in values]
        maximums = [cpt.loc[index] for index in indices]
        cpt = pd.concat(maximums, axis=1).transpose().reset_index().drop('index', axis=1).dropna()

        for idx, row in cpt.iterrows():
            self._value_dict[variable] = cpt.to_dict('records')[idx][variable]

        cpt = cpt.drop(columns=variable, axis=1)

        return cpt

