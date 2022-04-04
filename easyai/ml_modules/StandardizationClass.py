import pandas as pd

from easyai.abstracts import AbstractEditDataFrameClass

class StandardizationClass(AbstractEditDataFrameClass):
    def __init__(self) -> None:
        super().__init__()


    def standard_all(self, df) -> pd.DataFrame:
        """
        渡されたdf全ての列に対して標準化を行う。

        Parameters
        ----------
        df : DataFrame
            カテゴリ変数変換まで行ったdf

        returns
        -------
        df : DataFrame
            標準化を行ったdf
        """
        self.set_backup_df(df)
        
        stats = df.describe()
        stats = stats.transpose()
        return (df - stats['mean']) / stats['std']


    def standard_without_objective(self, df, objective_name) -> pd.DataFrame:
        """
        目的変数をのぞいて標準化を行う

        Parameters
        ----------
        df : DataFrame
            カテゴリ変数変換まで行ったdf

        objective_name : str
            目的変数列名

        returns
        -------
        df : DataFrame
            標準化を行ったdf
        """
        self.set_backup_df(df)

        objective = df.pop(objective_name)
        df = self.standard_all(df)
        df[objective_name] = objective
        return df


    def standard_predict_data(self, train, predict):
        stats = train.describe()
        stats = stats.transpose()
        return (predict - stats['mean']) / stats['std']