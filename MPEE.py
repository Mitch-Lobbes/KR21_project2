import itertools
from ordering import Ordering
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

    def run(self, bn: BayesNet, evidence: dict[str, bool]):
        self._bn = bn
        self._evidence = evidence

        self._edge_pruning()

        Q = self._bn.get_all_variables()
        ordered_Q = self._ordering.min_degree(bn=self._bn, X=Q)
        cpts = self._bn.get_all_cpts()
        S = list(cpts.values())

        #print('Evidence:', self._evidence)
        #print(f"Order: {ordered_Q}")
        ordered_Q = ['J','I', 'X', 'Y', 'O']
        #print(f"Order: {ordered_Q}")

        for maxoutvar in ordered_Q:
            #print('\nMaximising out:', maxoutvar)
            factors = self._cpts_containing_var(cpts=S, variable=maxoutvar)
            headers = [list(cpt.columns) for cpt in factors]
            product = self._multiply(factors=factors)
            new_cpt = self._super_max(cpt=product, variable=maxoutvar)
            #print(new_cpt)
            #print("-----------------------")

            S = [cpt for cpt in S if list(cpt.columns) not in headers]

            S.append(new_cpt)
            print(S)
            print("--------------------------")

        trivial = pd.DataFrame({'p': [1.0], 'MPE': [{}]})
        for f in S:
            trivial.iloc[0]['MPE'].update(f.iloc[0]['MPE'])
            trivial.at[0,'p'] = trivial.iloc[0]['p'] * f.iloc[0]['p']

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

    def _multiply(self, factors: list[pd.DataFrame]) -> pd.DataFrame:

        common_vars = reduce(np.intersect1d, ([factor.columns for factor in factors]))
        common_vars = np.delete(common_vars, np.where(common_vars == 'p'))
        if 'MPE' in common_vars:
            common_vars = np.delete(common_vars, np.where(common_vars == 'MPE'))

        merged_df = pd.DataFrame()
        for factor in factors:
            if merged_df.empty:
                merged_df = factor
            else:
                merged_df = pd.merge(merged_df, factor, on=list(common_vars))
                merged_df['p'] = (merged_df['p_x'] * merged_df['p_y'])
                merged_df.drop(['p_x', 'p_y'], inplace=True, axis=1)
        for common_var in common_vars:
            merged_df[common_var] = merged_df[common_var].astype('bool')
        merged_df['p'] = merged_df['p'].astype(float)
        #print('Product of factors:\n', merged_df)
        return merged_df


    def _multi_fly(self, factors: list[pd.DataFrame]) -> pd.DataFrame:
        if len(factors) == 1:
            return factors[0]

        columns = set()
        for factor in factors:
            for col in factor.columns[:-1]:
                columns.add(col)

        table = list(itertools.product([False, True], repeat=len(columns)))
        df = pd.DataFrame(columns=sorted(columns), data=table)
        df['p'] = float(1.0)
        print('Empty df:\n', df)

        df = self._bn.get_compatible_instantiations_table(instantiation=pd.Series(self._evidence), cpt=df)

        for idx, row in df.iterrows():
            vars, values, p_values = [], [], []
            for var, value in row[:-1].items():
                vars.append(var)
                values.append(value)
            instantiation = pd.Series(data=values, index=vars)
            print(f"Z Instantiation:\n {instantiation}")

            for factor in factors:
                print('Factor:\n', factor)
                compatible = self._bn.get_compatible_instantiations_table(instantiation=instantiation, cpt=factor)
                print('Compatible instantiation in X:\n', compatible)
                #print("--------------")
                p_values.append(float(compatible['p']))

            p = np.prod(p_values)
            df.at[idx, 'p'] = p
            print('Result of multifly:\n', df)

        return df

    def _super_max(self, cpt: pd.DataFrame, variable: str):

        indices = []
        truth = cpt[variable].unique()

        for value in truth:
            indices.append(cpt.loc[cpt[variable] == value]['p'].idxmax())

        maximums = [cpt.loc[index,: ] for index in indices]
        #print('Maximums:\n', maximums)
        cpt = pd.concat(maximums, axis=1).transpose().reset_index().drop('index', axis=1).dropna()

        if 'MPE' not in cpt.columns:
            row_count = cpt.shape[0]
            dicts = [{} for number in range(row_count)]
            cpt.loc[:,'MPE'] = dicts

        for idx, row in cpt.iterrows():
            for var, value in row.items():
                if var == variable:
                    cpt.at[idx,'MPE'][variable] = value

        cpt = cpt.drop(columns=variable, axis=1)
        #print('Return from Supermax:\n', cpt)
        return cpt

    def _cpts_containing_var(self, cpts: list[pd.DataFrame], variable: str) -> list[pd.DataFrame]:
        return [cpt for cpt in cpts if variable in cpt.columns]
