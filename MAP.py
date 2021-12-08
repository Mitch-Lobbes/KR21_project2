import copy

from BayesNet import BayesNet
from BayesNet import BayesNet
from typing import Set
import pandas as pd


class MAP:

    def __init__(self):
        pass

    def sum_out_new

    def sum_out(self, bn: BayesNet, node: str) -> None:
        cpt = bn.get_all_cpts()
        dfs_containing_var = [val for key, val in cpt.items() if node in val]
        var_cpt = bn.get_cpt(node)

        # node_df = [dataframe for dataframe in dfs_containing_var if node == dataframe.keys()[-2]][0]

        # Check if DF is solely dependant on the wanted variable
        if len(var_cpt.columns) != 2:
            # Recursively sum out other variables
            for i in range(len(var_cpt.columns) - 2):
                self.sum_out(
                    bn=bn,
                    node=var_cpt.columns[i]
                )

        dfs_containing_var.remove(var_cpt)

        var_value_true = var_cpt.loc[var_cpt[node] is True]['p']
        var_value_false = var_cpt.loc[var_cpt[node] is False]['p']

        # MULTIPLY VALUES
        for df in dfs_containing_var:
            self._multiply_rows_with_value(
                df=df,
                variable=node,
                true_value=var_value_true,
                false_value=var_value_false
            )

        # SUM ROWS
        for df in dfs_containing_var:
            column_names = [key for key in df if key != node]
            new_df = pd.DataFrame(columns=column_names)
            for index, row in df.iterrows():
                corresponding_row = self._search_correspinding_row(
                    df=df,
                    row=row,
                    key_var=node
                )
                corresponding_row.at['p'] += corresponding_row['p'] # Does this work?
                new_df.append(copy.deepcopy(corresponding_row))
                df.drop(index=corresponding_row.index[0])
            df = new_df
        print(df)

        return bn, df.columns[0]

    def _multiply_rows_with_value(self, df, variable, true_value, false_value):
        for index, row in df.iterrows():
            val = true_value if row[variable] is True else false_value
            df.at[index, 'p'] *= val

    def _search_correspinding_row(self, df, row, key_var):

        res_row = df.loc[df[key_var] == (not row[key_var])]
        res_row.drop(key_var, 1, inplace=True)

        for key in res_row:
            res_row = res_row.loc[df[key] == row[key]]

        return res_row

        # result_row = df.loc[df[node] == not node_value].loc[df['I'] == False].loc[df['X'] == False]
        # index = x.loc[x['J'] == True].loc[x['I'] == False].loc[x['X'] == False].index[0]    

    def super_max(self, cpt: pd.DataFrame, variable: str):

        s1 = cpt.loc[cpt[variable] == True].max().to_frame()
        s2 = cpt.loc[cpt[variable] == False].max().to_frame()

        cpt = pd.concat([s1, s2], axis=1).reset_index().transpose()

        return cpt

    def multi_fly(self):
        pass
    
    def sum_out_var(cpt: pd.DataFrame, variable: str) -> pd.DataFrame:
        pass
