from BayesNet import BayesNet
import pandas as pd

class MAP:

    def __init__(self):
        pass

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
        for df in dfs_containing_var:
            for index, row in df.iterrows():
                val = var_value_true if row[node] is True else var_value_false
                df.at[index, 'p'] *= val

        

        # Sum up rows
        for df in dfs_containing_var:

            column_names = [key for key in df if key != node]
            new_df = pd.DataFrame(columns = column_names)

            for index, row in df.iterrows():
                result_row, result_counter = find_corresponding_row(
                    df = df,
                    row = row,
                    variable_tuple = (node, not row[node])
                )
                new_p = row['p'] + result_row['p']
                new_df.insert(loc=index, column="p", value=new_p)
                # delete result_row?
                new_df.drop(df.index[[result_counter]])


    def find_corresponding_row(self, df, row, variable_tuple):
        row_dict  = row.to_dict()
        del row_dict["p"]
        result_row = df.loc[df[variable_tuple[0]] == variable_tuple[1]]
        counter = 0
        for key, value in row.items():
            result_row = result_row.loc[df[key] == value]
            row_counter = result_row.loc[df[key] == value].index[0]
        return result_row, row_counter



       
