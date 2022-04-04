import os
import time

import pandas as pd

from easyai.other_modules import SingletonClass

class UploaderClass(SingletonClass):
    ROOT = 'C:/Users/kt/Desktop/project3/pr3/easyai/static/easyai/'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self) -> None:
        self.upload_path = {}

    def set_last_upload_path(self, user_id, path):
        """
        最後にアップロードしたパスを格納する。
        """
        self.upload_path[user_id] = path

    def get_last_upload_path(self, user_id):
        return self.upload_path[user_id]


    def make_dir(self, path):
        """
        渡されたパスでディレクトリ作成
        """
        os.makedirs(UploaderClass.ROOT+path, exist_ok=True)

    def seve_as_csv(self, user_id, path, data):
        """
        特定のデータをcsvとして保存
        """
        self.set_last_upload_path(user_id, path)
        with open(UploaderClass.ROOT+path, mode='w') as f:
            for chunk in data.chunks():
                chunk = chunk.decode('UTF-8').replace('\n', '')
                f.write(chunk)


    def seve_as_csv_tmp(self, user_id, path, data):
        """
        特定のデータをcsvとして一時保存
        """
        with open(UploaderClass.ROOT+path, mode='w') as f:
            for chunk in data.chunks():
                chunk = chunk.decode('UTF-8').replace('\n', '')
                f.write(chunk)

    def make_now_time_path(self):
        """
        現在時刻を元にしたファイル名を生成する。
        """
        return str(time.time_ns())
