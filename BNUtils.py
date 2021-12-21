import pandas as pd
import copy

class BNUtils:

    @staticmethod
    def sum_out_var(cpt: pd.DataFrame, variable: str) -> pd.DataFrame:
        """Sum out a variable from a conditional probability table (CPT)

        Args:
            cpt (pd.DataFrame): Pandas DataFrame representation of the cpt
            variable (str): Variable to sum out

        Returns:
            pd.DataFrame: cpt after summing out the variable
        """
        cpt = copy.deepcopy(cpt)
        mask = cpt[variable] == True
        var_true_df = cpt[mask].drop(variable, axis=1)
        var_false_df = cpt[~mask].drop(variable, axis=1)

        columns = [col for col in var_true_df.columns if col != 'p']

        resulting_df = pd.concat([var_true_df, var_false_df]).groupby(columns, as_index=False)["p"].sum()
        cpt = resulting_df
        return resulting_df

    @staticmethod
    def multiply_factors(cpt1: pd.DataFrame, cpt2: pd.DataFrame) -> pd.DataFrame:
        """Multiply two given factors

        Args:
            cpt1 (pd.DataFrame): Pandas DataFrame representation of first cpt
            cpt1 (pd.DataFrame): Pandas DataFrame representation of second cpt

        Returns:
            pd.DataFrame: cpt after multiplying cpt1 and cpt2
        """
        cpt1 = copy.deepcopy(cpt1)
        cpt2 = copy.deepcopy(cpt2)
        common_vars = list(
            set([col for col in cpt1.columns if col != 'p']) & set([col for col in cpt2.columns if col != 'p']))
        if not common_vars:
            return pd.merge(cpt1, cpt2, on=['p'])
        merged_df = pd.merge(cpt1, cpt2, on=common_vars)
        merged_df['p'] = (merged_df['p_x'] * merged_df['p_y'])
        merged_df.drop(['p_x', 'p_y'], inplace=True, axis=1)

        return merged_df
