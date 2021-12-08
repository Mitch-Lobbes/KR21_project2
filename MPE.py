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
        print(self._evidence)

        for k,v in self._bn.get_all_cpts().items():
            print(k,v)

        self._edge_pruning()

        for k,v in self._bn.get_all_cpts().items():
            print(k,v)

        raise SystemExit

        Q = self._bn.get_all_variables()
        ordered_Q = self._ordering.min_degree(bn=self._bn, X=Q)
        cpts = self._bn.get_all_cpts()
        print(f"Evidence: {self._evidence}")

        for var, cpt in cpts.items():
            new_cpt = self._bn.get_compatible_instantiations_table(instantiation=pd.Series(self._evidence), cpt=cpt)
            self._bn.update_cpt(variable=var, cpt=new_cpt)

        print(f"Order: {ordered_Q}")

        for variable in ordered_Q:
            df_list = []
            for cptippie in cpts.values():
                if variable in cptippie.columns:
                    df_list.append(cptippie)

            f = self.multi_fly(factors=df_list)
            print('THIS IS F________')
            print(f)
            cpt = self.super_max(cpt=f, variable=variable)

            print('THIS IS MAX________')
            print(cpt)
            raise SystemExit

    def _edge_pruning(self):

        for edge_list in [self._bn.get_edges_outgoing_from_var(variable=le_element) for le_element in
                          self._evidence]:

            print(f"----------------------------{edge_list}")


            self._bn.del_edges(edges=edge_list)


            for edge in edge_list:
                #print(f"----------------------------{edge}")
                u = edge[0]
                value = self._evidence[u]
                x = edge[1]

                cpt = self._bn.get_cpt(variable=x)
                print("CPT:\n", cpt)
                new_cpt = self._bn.get_compatible_instantiations_table(
                    instantiation=pd.Series(data={u: value}, index=[u]), cpt=cpt)
                print("new CPT:\n", new_cpt)

                cpt = self._bn.get_cpt(variable=u)
                print(f"---{pd.Series(data={u: value}, index=[u])}")
                new_cpt = self._bn.get_compatible_instantiations_table(
                    instantiation=pd.Series(data={u: value}, index=[u]), cpt=cpt)

                raise SystemExit
                # for var in self._evidence.keys():
                #     if var in new_cpt.columns and var != x:
                #
                #         new_cpt = new_cpt.drop(var, axis=1)

                self._bn.update_cpt(variable=x, cpt=new_cpt)

    def multi_fly(self, factors: list[pd.DataFrame]) -> pd.DataFrame:
        print(*factors, sep="\n\n")
        columns = set()

        for factor in factors:
            for col in factor.columns[:-1]:
                columns.add(col)

        table = list(itertools.product([False, True], repeat=len(columns)))
        df = pd.DataFrame(columns=sorted(columns), data=table)
        df['p'] = float(1.0)
        print(df)
        for idx, row in df.iterrows():
            vars, values, p_values = [], [], []

            for var, value in row[:-1].items():
                vars.append(var)
                values.append(value)

            instantiation = pd.Series(data=values, index=vars)
            print(f"instantiation: {instantiation}")

            for factor in factors:
                compatible = self._bn.get_compatible_instantiations_table(instantiation=instantiation, cpt=factor)
                print(compatible)
                print("--------------")
                p_values.append(float(compatible['p']))

            p = np.prod(p_values)
            df.at[idx, 'p'] = p

        return df

    def super_max(self, cpt: pd.DataFrame, variable: str):

        s1 = cpt.loc[cpt[variable] == True].max().to_frame()
        s2 = cpt.loc[cpt[variable] == False].max().to_frame()

        cpt = pd.concat([s1, s2], axis=1).reset_index().transpose()

        return cpt
