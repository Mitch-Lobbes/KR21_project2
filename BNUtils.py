import pandas as pd


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
        if not variable in cpt or len(cpt.columns) == 2:
            return
        mask = cpt[variable] == True
        var_true_df = cpt[mask].drop(variable, axis=1)
        var_false_df = cpt[~mask].drop(variable, axis=1)

        columns = [col for col in var_true_df.columns if col != 'p']

        resulting_df = pd.concat([var_true_df, var_false_df]).groupby(columns, as_index=False)["p"].sum()
        return resulting_df
