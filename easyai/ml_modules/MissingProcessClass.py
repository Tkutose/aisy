from typing import List
import pandas as pd

from easyai.abstracts import AbstractEditDataFrameClass

class MissingProcessClass(AbstractEditDataFrameClass):
    """
    欠損値処理用クラス
    """

    def __init__(self) -> None:
        super().__init__()


    def get_numeric_column_names(self, df) -> List[str]:
        """
        dfのデータタイプが数値型の列名を返す

        Parameters
        ----------
        df : DataFrame
            未処理でもok

        returns
        -------
        : list
            dfのデータタイプが数値型の列名を格納したlist
        """
        return [col for col in df.columns if df[col].dtype != 'object']


    def get_outlier_options(self, df) -> List[str]:
        """
        大きく外れた値を列ごとにdictに格納して返す

        Parameters
        ----------
        df : DataFrame
            未処理でもok

        returns
        -------
        outliers : dict
            大きく外れた値
            (low: 第一四分位数 - 四分位範囲 * 5)
            (high: 第三四分位数 + 四分位範囲 * 5)
            をそれぞれ超えた値を外れ値候補とする
        """
        outliers = {}
        numeric_cols = self.get_numeric_column_names(df)
        for col in numeric_cols:
            q1 = df[col].sum()/len(df[col]) * 1
            q3 = df[col].sum()/len(df[col]) * 3
            iqr = q3 - q1
            low = q1 - iqr * 5.0
            high = q3 + iqr * 5.0
            outliers[col] = [value for value in df[col]
                            if (value < low) or (value > high)]
        return outliers


    def get_missing_columns(self, df) -> dict:
        """
        欠損値を含む列のうち、欠損値が存在する割合が30%以下の埋めたほうが良いカラム名と、
        その埋める候補を返す。

        Parameters
        ----------
        df : DataFrame
            カテゴリ変数以外の文字が除去されたdf

        returns
        -------
        in_missing_columns : dict
            欠損値が1以上、30%以下のカラム名をkeyとし、
            valueにはその欠損値を埋める候補を
            文字列ならmode(最頻値)
            数値ならmean(平均値)、median(中央値)、mode(最頻値)
            と格納したdict
        """

        in_missing_columns = {}

        for col in df.columns:
            if df[col].isnull().sum() != 0:

                # 欠損値が30%以下なら、埋める推奨
                if df[col].isnull().sum() <= len(df)*0.7:
                    if df[col].dtype == 'object':
                        in_missing_columns.setdefault(
                            col, {'mode': df[col].mode().tolist()})
                    else:
                        in_missing_columns.setdefault(col,
                                                    {'mean': round(df[col].mean(),3),
                                                    'median': df[col].median(),
                                                    'mode': df[col].mode().tolist()
                                                    })
        return in_missing_columns


    def get_delete_columns(self, df) -> dict:
        """
        欠損値を含む列のうち、欠損値が存在する割合が70%以上の削除した方が良いが良いカラム名と、
        もし埋める場合用のその埋める候補を返す。

        Parameters
        ----------
        df : DataFrame
            カテゴリ変数以外の文字が除去されたdf

        returns
        -------
        delete_columns : dict
            欠損値が全体の70%より多いカラム名をkeyとし、
            valueにはその欠損値を埋める候補を
            文字列ならmode(最頻値)
            数値ならmean(平均値)、median(中央値)、mode(最頻値)
            と格納したdict
        """

        delete_columns = {}
        for col in df.columns:
            if df[col].isnull().sum() != 0:

                # 欠損値が70%以上あれば削除推奨
                if df[col].isnull().sum() > len(df)*0.7:
                    if df[col].dtype == 'object':
                        delete_columns.setdefault(
                            col, {'mode': df[col].mode().tolist()})
                    else:
                        delete_columns.setdefault(col,
                                                {'mean': round(df[col].mean(), 3),
                                                'median': df[col].median(),
                                                'mode': df[col].mode().tolist()
                                                })
                        delete_columns.append(
                            {col: {'mode': df[col].mode().tolist()}})
        return delete_columns


    def fill_value(self, df, col_name, value) -> pd.DataFrame:
        """
        dfの指定された列の欠損値を指定の値で埋める。

        Parameters
        ----------
        df : DataFrame
            カテゴリ変数以外の文字が除去されたdf

        col_name : str
            対象の列名

        value : int
            埋める値

        returns
        -------
        df : DataFrame
            指定された方法で欠損値を埋めたdf
        """
        self.set_backup_df(df)
        dtype = df[col_name].dtypes
        try:
            df[col_name] = df[col_name].fillna(value)
        except KeyError as e:
            print('fill_missing 列名が間違っています。')
        try:
            df[col_name] = df[col_name].astype(dtype)
        except TypeError as e:
            pass
        return df
