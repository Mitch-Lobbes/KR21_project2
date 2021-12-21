import itertools
from Ordering import Ordering
from BayesNet import BayesNet
from typing import Set
import pandas as pd
import numpy as np
from functools import reduce
import random

class MPE:

    def __init__(self):
        self._bn: BayesNet
        self._evidence: dict[str, bool]
        self._ordering = Ordering()
        self._value_dict = {}

    def run(self, bn: BayesNet, evidence: dict[str, bool], order):
        self._bn = bn
        self._evidence = evidence
        #self._bn.draw_structure()

        self._edge_pruning()

        query = self._bn.get_all_variables()
        ordered_query = self._ordering.min_fill(bn=self._bn, X=query)
        ordered_query = order
        print(ordered_query)
        #ordered_query = order
        #ordered_query = order
        #print(f"ORDER: {order}")
        #print(ordered_query)

        #ordered_query2 = self._ordering.min_degree(bn=self._bn, X=query)
        #print(ordered_query2)

        #random.shuffle(query)
        #print(query)

        cpt_list = list(self._bn.get_all_cpts().values())
        print(*cpt_list, sep="\n\n")
        print("START FOR LOOP")

        for variable in ordered_query:
            factors = self._all_cpt_containing_var(cpt_list=cpt_list, variable=variable)
            print(*factors, sep="\n\n")

            headers = [list(cpt.columns) for cpt in factors]
            product = self._multiply(factors=factors)

            new_cpt = self._super_max(cpt=product, variable=variable)
            print("--------------------------------------------------------------")

            cpt_list = [cpt for cpt in cpt_list if list(cpt.columns) not in headers]

            cpt_list.append(new_cpt)

        # trivial = pd.DataFrame({'p': [1.0], 'MPE': [self._value_dict]})
        # trivial['p'] = [cpt_list[i].iloc[0]['p']*cpt_list[i+1].iloc[0]['p'] for i in range(len(cpt_list)-1)]

        trivial = pd.DataFrame({'p': [1.0]})

        for f in cpt_list:
            #trivial.iloc[0]['MPE'].update(f.iloc[0]['MPE'])
            print(trivial)
            print(f)
            print("----")
            trivial.at[0,'p'] = trivial.iloc[0]['p'] * f['p'].max()

        print(f'\nThis is the MPE given the evidence {self._evidence}: \n {trivial}')
        for k, v in self._value_dict.items():
            print(k, v)

        self._value_dict = {}
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
        #common_vars = reduce(np.intersect1d, ([factor.columns for factor in factors]))
        #common_vars = list(np.delete(common_vars, np.where(common_vars == 'p')))
        #print(f"Common Vars: {common_vars}")

        merged_df = factors[0]

        for factor in factors[1:]:
            common_vars = np.intersect1d(merged_df.columns[:-1], factor.columns[:-1])
            print(f"Common vars: {common_vars}")
            merged_df = pd.merge(merged_df, factor, on=list(common_vars))
            merged_df['p'] = (merged_df['p_x'] * merged_df['p_y'])
            merged_df.drop(['p_x', 'p_y'], inplace=True, axis=1)

        merged_df['p'] = merged_df['p'].astype(float)
        print(f"Result of multiplication")
        print(merged_df)

        return merged_df

    def _super_max(self, cpt: pd.DataFrame, variable: str):

        cols = [col for col in cpt.columns[:-1] if col != variable]
        print(f"cols: {cols}")
        values = cpt[variable].unique() if len(cols) == 0 else cpt[cols[0]].unique()

        if len(cols) != 0:
            unique_vals = cpt.groupby(cols, as_index=False).size().drop(columns="size", axis=1)
            print(unique_vals)
            print(cpt[cols])

            unique_vals['p'] = [cpt[cpt[cols].apply(lambda x: x.equals(row[1]), axis=1)]['p'].max() for row in unique_vals.iterrows()]
            print(unique_vals)
            for idx, row in cpt.iterrows():
                self._value_dict[variable] = cpt.to_dict('records')[idx][variable]

            return unique_vals


            # for idx, row in unique_vals.iterrows():
            #     #print(row)
            #     print(cpt[cpt[cols].apply(lambda x: x.equals(row), axis=1)]['p'].max())
            #     print(cpt[cpt[cols].apply(lambda x: x.equals(row), axis=1)])
            #selectedType = cpt[cpt[cols] == unique_vals.columns]
            #print(selectedType)
            #selectedTypeAndYear = selectedType.loc[selectedType["Year"] == selectedType["Year"].max(), :]
            #maxValue = selectedTypeAndYear["Number"].max()

        print(f"Variable: {variable}")
        print(f"Values: {values}")
        var = variable if len(cols) == 0 else cols[0]
        indices = [cpt.loc[cpt[var] == value]['p'].idxmax() for value in values]
        maximums = [cpt.loc[index] for index in indices]
        cpt = pd.concat(maximums, axis=1).transpose().reset_index().drop('index', axis=1).dropna()

        for idx, row in cpt.iterrows():
            self._value_dict[variable] = cpt.to_dict('records')[idx][variable]

        cpt = cpt.drop(columns=variable, axis=1)
        print(f"Result of maximize: {variable}")
        print(cpt)

        return cpt

    def _multi_fly(self, factors: list[pd.DataFrame]) -> pd.DataFrame:
        print(*factors, sep="\n\n")

        if len(factors) == 1:
            print("------------------------------------")
            return factors[0]

        columns = set()
        for factor in factors:
            for col in factor.columns[:-1]:
                columns.add(col)
        table = list(itertools.product([False, True], repeat=len(columns)))
        df = pd.DataFrame(columns=sorted(columns), data=table)
        df['p'] = float(1.0)

        #print('Empty df:\n', df)

        df = self._bn.get_compatible_instantiations_table(instantiation=pd.Series(self._evidence), cpt=df)
        print(df)

        for idx, row in df.iterrows():
            vars, values, p_values = [], [], []
            for var, value in row[:-1].items():
                vars.append(var)
                values.append(value)
            instantiation = pd.Series(data=values, index=vars)
            #print(f"Z Instantiation:\n {instantiation}")

            for factor in factors:
                #print('Factor:\n', factor)
                compatible = self._bn.get_compatible_instantiations_table(instantiation=instantiation, cpt=factor)
                #print('Compatible instantiation in X:\n', compatible)
                #print("--------------")
                p_values.append(compatible['p'].astype(float))

            p = np.prod(p_values)
            df.at[idx, 'p'] = p
            #print('Result of multifly:\n', df)
        print("------------------------------------")
        return df

