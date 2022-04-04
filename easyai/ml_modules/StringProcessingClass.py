from typing import List

import pandas as pd

from easyai.abstracts import AbstractEditDataFrameClass

class StringProcessingClass(AbstractEditDataFrameClass):
    def __init__(self) -> None:
        return super().__init__()

    def get_recommend_delete_columns(self, df) -> List[str]:
        """
        カテゴリ変数に変換できる閾値を10とし、11以上のユニーク値が含まれる列を削除推奨列として返す

        Parameters
        ----------
        df : DataFrame
            未処理でもok

        returns
        -------
        delete_recommend_cols : list
            ユニーク値が11以上ある削除推奨列名
        """

        delete_recommend_cols = []
        for col in df.columns:
            if df[col].dtype == 'object' and len(df[col].unique()) > 10:
                delete_recommend_cols.append(col)
        return delete_recommend_cols

    def get_string_column_names(self, df) -> List[str]:
        """
        dfのデータタイプが文字列型(object)の列名を返す

        Parameters
        ----------
        df : DataFrame
            未処理でもok

        returns
        -------
        : list
            dfのデータタイプがobject型の列名を格納したlist
        """
        return [col for col in df.columns if df[col].dtype == 'object']


    def delete_one_column(self, df, col_name) -> pd.DataFrame:
        """
        1列削除する。

        Parameters
        ----------
        df : DataFrame
            未処理でもok

        col_name : str
            削除したい列名

        returns
        -------
        df : DataFrame
            col_name列を削除したdf
        """

        self.set_backup_df(df)
        try:
            df = df.drop(col_name, axis=1)
        except KeyError as e:
            print('delete_one_column 列名が間違っています。')
        return df


    def delete_any_column(self, df, col_names) -> pd.DataFrame:
        """
        複数列削除する。

        Parameters
        ----------
        df : DataFrame
            未処理でもok

        col_names : list
            削除したい複数列名

        returns
        -------
        df : DataFrame
            col_names列を削除したdf
        """
        self.set_backup_df(df)
        try:
            df = df.drop(col_names, axis=1)
        except KeyError as e:
            print('列名が間違っています。')
        return df


    def delete_one_str_value(self, df, col_name, value, is_regex=True) -> pd.DataFrame:
        """
        列中の文字列を空白文字に置き換える(削除)

        Parameters
        ----------
        df : DataFrame
            未処理でもok

        col_name : str
            対象の列名

        value : str
            削除する文字列

        is_regex : bool
            default=True
            部分一致検索で削除するかどうか(本来は正規表現を使用するかどうか)

        returns
        -------
        df : DataFrame
            col_name列に含まれるvalueを削除したdf
        """
        self.set_backup_df(df)
        try:
            df[col_name] = df[col_name].replace(value, '', regex=is_regex)
        except KeyError as e:
            print('列名が間違っています。')
        return df


    def delete_any_str_value(self, df, col_name, delete_tuple, is_regex=True) -> pd.DataFrame:
        """
        列中の文字列を複数指定し、空白文字に置き換える(削除)

        Parameters
        ----------
        df : DataFrame
            未処理でもok

        col_name : str
            対象の列名

        delete_tuple : tuple
            削除する文字列を複数含んだtuple

        is_regex : bool
            default=True
            部分一致検索で削除するかどうか(本来は正規表現を使用するかどうか)

        returns
        -------
        df : DataFrame
            col_name列に含まれるdelete_tupleを削除したdf
        """
        self.set_backup_df(df)

        try:
            df[col_name] = df[col_name].replace(delete_tuple, '', regex=is_regex)
        except KeyError as e:
            print('列名が間違っています。')
        return df


    def replace_str_value(self, df, col_name, before, after, is_regex=True) -> pd.DataFrame:
        """
        列中の文字列を置換する

        Parameters
        ----------
        df : DataFrame
            未処理でもok

        col_name : str
            対象の列名

        before : str
            置換前文字列

        after : str
            置換後文字列

        returns
        -------
        df : DataFrame
            col_name列に含まれるbeforeをafterに置換したdf
        """
        
        self.set_backup_df(df)
        try:
            df[col_name] = df[col_name].replace(before, after, regex=is_regex)
        except KeyError as e:
            print('replace_str_value 列名が間違っています。')
        return df
