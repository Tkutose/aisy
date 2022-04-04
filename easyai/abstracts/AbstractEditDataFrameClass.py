from abc import ABCMeta


class AbstractEditDataFrameClass(metaclass=ABCMeta):
    """
    DataFrameに変更を及ぼすクラス用の抽象基底クラス
    """
    def __init__(self) -> None:
        self.backup_df = None

    def set_backup_df(self, df):
        self.backup_df = df

    def get_before_df(self):
        """
        直近の変更前のdfを返す
        """
        return self.backup_df
