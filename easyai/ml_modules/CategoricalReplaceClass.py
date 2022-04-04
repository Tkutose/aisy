from typing import List

import pandas as pd
import numpy as np

from easyai.abstracts import AbstractEditDataFrameClass

class CategoricalReplaceClass(AbstractEditDataFrameClass):
    def __init__(self) -> None:
        return super().__init__()

    def get_isnot_number_column_name(self, df) -> List[str]:
        """
        dfから数字でないデータ型の列名を取得する

        Parameters
        ----------
        df : DataFrame
            未処理でもok
        
        returns
        -------
        columns : list
            dfのうち、データ型が数字でない列(object)の列名が格納されているlist
        """

        categorical_columns = []
        for col in df.columns:
            if df[col].dtype == 'object':
                categorical_columns.append(col)
        return categorical_columns


    def label_encoding(self, df, column_name) -> pd.DataFrame:
        """
        該当行のlabel encodingを行う。
        
        Parameters
        ----------
        df : DataFrame
            カテゴリ変数以外の文字データ・欠損値が処理されたdf

        column_name : str 
            列名

        returns
        -------
        df : DataFrame
        カテゴリ変数をlabel encodingしたdf
        """
        self.set_backup_df(df)
        self.history = []
        values = [value for value in df[column_name].unique() if str(value)!='nan']
        for value, num in zip(values, range(len(values))):
            df = df.replace({column_name: {value: num}})
            self.history.append({'before':value, 'after': num})
        return df

    def get_history(self) -> list:
        """
        1つ前のカテゴリ変数変換にて行った変換一覧を取得する
        (主にDB格納用)
        beforeに変換前,afterに変換後の値が格納されたdict群

        例 [{'before':'female', 'after':0}, {'before':'male', 'after':1}]
        """
        return self.history

    def replace_categorical(self, df) -> pd.DataFrame:
        """
        カテゴリ変数を変換する。
        
        Parameters
        ----------
        df : DataFrame
            カテゴリ変数以外の文字データ・欠損値が処理されたdf

        returns
        -------
        df : DataFrame
        カテゴリ変数をlabel encodingしたdf
        """

        # カテゴリ変数の列を取得
        categorical_columns = self.get_isnot_number_column_name(df)

        # 取得した列ごとに値を変換していく
        df = self.label_encoding(df, categorical_columns)

        return df
