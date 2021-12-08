import itertools
from ordering import Ordering
from BayesNet import BayesNet
from typing import Set
import pandas as pd
import numpy as np

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

        print(f"Order: {ordered_Q}")
        ordered_Q = ['J', 'I', 'X', 'Y', 'O']
        print(f"Order: {ordered_Q}")



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

    def _multi_fly(self, factors: list[pd.DataFrame]) -> pd.DataFrame:
        if len(factors) == 1:
            return factors[0]
        #print(*factors, sep="\n\n")

        columns = set()

        for factor in factors:
            for col in factor.columns[:-1]:
                columns.add(col)

        table = list(itertools.product([False, True], repeat=len(columns)))
        df = pd.DataFrame(columns=sorted(columns), data=table)
        df['p'] = float(1.0)

        df = self._bn.get_compatible_instantiations_table(instantiation=pd.Series(self._evidence), cpt=df)

        for idx, row in df.iterrows():
            vars, values, p_values = [], [], []

            for var, value in row[:-1].items():
                vars.append(var)
                values.append(value)

            instantiation = pd.Series(data=values, index=vars)
            #print(f"instantiation: {instantiation}")

            for factor in factors:
                compatible = self._bn.get_compatible_instantiations_table(instantiation=instantiation, cpt=factor)
                #print(compatible)
                #print("--------------")
                p_values.append(float(compatible['p']))

            p = np.prod(p_values)
            df.at[idx, 'p'] = p

        return df

    def _super_max(self, cpt: pd.DataFrame, variable: str):

        s1 = cpt.loc[cpt[variable] == True].max().to_frame()
        s2 = cpt.loc[cpt[variable] == False].max().to_frame()

        #print(s1.transpose())
        #print("\n")
        #print(s2.transpose())
        #print("\n")

        cpt = pd.concat([s1, s2], axis=1).transpose().reset_index().drop('index', axis=1).dropna()

        return cpt

