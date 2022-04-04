from typing import Tuple

from sklearn.model_selection import train_test_split
import pandas as pd


class SplitDataClass():
    def split_objective_variable(self, df, objective_column_name) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        dfから目的変数を切り離して返す

        Parameters
        ----------
        df : DataFrame
            各種処理済df
        objective_column_name : str
            目的変数の列名

        returns
        -------
        train_x : DataFrame
            目的変数を切り離したdf
        train_y : DataFrame
            目的変数のみのdf
        """
        train_y = df.pop(objective_column_name)
        train_x = df.copy()
        return train_x, train_y

    def validate_split(self, train_x, train_y, valid_size=0.33, random_state=71) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        trainとvalidationに分割して返す

        Parameters
        ----------
        train_x : DataFrame
            目的変数以外が格納された処理済df

        train_y : DataFrame
            目的変数が格納されたdf

        test_size : float
            default 0.33
            validの分割割合
            デフォルトでは33%がvalidationに使われる

        random_state : int
            default 71
            分割に使用する値
            同じ数を指定すれば分割に再現性が保てる

        returns
        -------
        return train_test_split() : tuple
            trainの目的変数以外, validationの目的変数以外, trainの目的変数, validationの目的変数
        """
        return train_test_split(train_x, train_y, test_size=valid_size, random_state=random_state, shuffle=True)



    def split(self, df, objective_column_name, valid_size=0.33, random_state=71) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        trainとvalidationに分割して返す

        Parameters
        ----------
        df : DataFrame
            目的変数以外が格納された処理済df

        objective_column_name : str
            目的変数の列名

        test_size : float
            default 0.33
            validの分割割合
            デフォルトでは33%がvalidationに使われる

        random_state : int
            default 71
            分割に使用する値
            同じ数を指定すれば分割に再現性が保てる

        returns
        -------
        train_x : DataFrame
            trainの目的変数以外

        valid_x : DataFrame
            validationの目的変数以外
        
        train_y : DataFrame
            trainの目的変数

        valid_y : DataFrame
            validationの目的変数
        """

        train_x, train_y = self.split_objective_variable(df, objective_column_name)
        train_x, valid_x, train_y, valid_y = self.validate_split(
            train_x, train_y, valid_size=valid_size, random_state=random_state)

        return train_x, valid_x, train_y, valid_y
